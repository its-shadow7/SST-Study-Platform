/**
 * Vercel Routing Middleware
 * Protects all /data/** paths before CDN cache lookup.
 * Reference: Section 3 & 4 of Antigravity Study Platform TDD v1.1
 *
 * JWT enforcement:
 *   - Algorithm : RS256
 *   - Required header: kid (non-empty)
 *   - Required claims: sub (non-empty), iss, aud, exp, iat, jti
 *   - Clock tolerance: 10 s (handles minor server skew)
 */

import { importSPKI, jwtVerify, decodeProtectedHeader } from 'jose';

// Cached imported public key instance for warm runtime performance
let cachedPublicKey: CryptoKey | null = null;

async function getPublicKey(): Promise<CryptoKey | null> {
  if (cachedPublicKey) return cachedPublicKey;

  const b64 = process.env.JWT_PUBLIC_KEY_B64;
  if (!b64) {
    console.error('[Middleware] JWT_PUBLIC_KEY_B64 is not set in environment.');
    return null;
  }

  try {
    const pem = Buffer.from(b64, 'base64').toString('utf-8');
    cachedPublicKey = (await importSPKI(pem, 'RS256')) as CryptoKey;
    return cachedPublicKey;
  } catch (err) {
    console.error('[Middleware] Failed to import public key:', err);
    return null;
  }
}

function parseCookies(cookieHeader: string | null): Record<string, string> {
  const cookies: Record<string, string> = {};
  if (!cookieHeader) return cookies;
  
  cookieHeader.split(';').forEach((cookie) => {
    const [name, ...rest] = cookie.trim().split('=');
    if (name) {
      cookies[name] = decodeURIComponent(rest.join('='));
    }
  });
  return cookies;
}

export default async function middleware(request: Request) {
  const url = new URL(request.url);

  // Match only /data/** paths
  if (!url.pathname.startsWith('/data/')) {
    return;
  }

  const cookieHeader = request.headers.get('cookie');
  const cookies = parseCookies(cookieHeader);
  const token = cookies['access_token'];

  const failResponse = (message: string, status = 401) => {
    return new Response(
      JSON.stringify({
        error: status === 403 ? 'FORBIDDEN' : (status === 503 ? 'SERVICE_UNAVAILABLE' : 'UNAUTHORIZED'),
        message,
        path: url.pathname,
        request_id: crypto.randomUUID()
      }),
      {
        status,
        headers: {
          'content-type': 'application/json',
          'cache-control': 'private, no-store'
        }
      }
    );
  };

  if (!token) {
    return failResponse('Valid SST student authentication required to view course notes.', 401);
  }

  const publicKey = await getPublicKey();
  if (!publicKey) {
    // Fail-closed if public key is missing or misconfigured
    return failResponse('Security configuration unavailable.', 503);
  }

  try {
    // ---- 1. Header checks (before signature verification) ----
    // Decode the protected header without verifying the signature yet.
    // This is safe: we only read metadata, not trust the payload.
    let header: Record<string, unknown>;
    try {
      header = decodeProtectedHeader(token) as Record<string, unknown>;
    } catch {
      return failResponse('Malformed JWT header.', 401);
    }

    // Enforce kid claim in header
    const kid = header['kid'];
    if (!kid || typeof kid !== 'string' || kid.trim() === '') {
      return failResponse('JWT is missing required key-ID (kid) header.', 401);
    }

    // ---- 2. Signature + registered-claims verification ----
    const expectedIssuer = process.env.JWT_ISSUER || 'sst-study-platform';
    const expectedAudience = process.env.JWT_AUDIENCE || 'sst-students';
    const { payload } = await jwtVerify(token, publicKey, {
      issuer: [expectedIssuer, 'antigravity-study-platform'],
      audience: [expectedAudience, 'antigravity-students'],
      clockTolerance: 10,          // 10-second tolerance for clock skew
      requiredClaims: ['sub', 'iss', 'aud', 'exp', 'iat', 'jti']
    });

    // ---- 3. Payload-level checks ----
    // sub must be non-empty
    if (!payload.sub || payload.sub.trim() === '') {
      return failResponse('JWT subject (sub) claim is empty.', 401);
    }

    // Role must be sst_student or admin (faculty accounts are blocked)
    const userRole = (payload as Record<string, unknown>)['role'];
    if (userRole !== 'sst_student' && userRole !== 'admin') {
      return failResponse('Insufficient permissions for study notes.', 403);
    }

    // ---- 4. Pass the request to the origin / CDN ----
    // Response must be private, no-store for browser; CDN may cache for authorized requests
    const response = new Response(null, {
      headers: {
        'x-middleware-next': '1',
        'cache-control': 'private, no-store',
        'vercel-cdn-cache-control': 'max-age=3600, s-maxage=3600'
      }
    });

    return response;
  } catch (err: unknown) {
    const errObj = err as { code?: string };
    const msg = errObj.code === 'ERR_JWT_EXPIRED'
      ? 'Access session expired. Please refresh your session.'
      : errObj.code === 'ERR_JWT_MISSING_REQUIRED_CLAIM'
        ? 'JWT is missing required claims.'
        : 'Invalid or forged authentication credentials.';
    return failResponse(msg, 401);
  }
}

export const config = {
  matcher: ['/data/:path*']
};
