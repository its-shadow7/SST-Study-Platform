import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { App } from './App';
import { AuthProvider } from '@/context/AuthContext';
import { BookmarkProvider } from '@/context/BookmarkContext';
import { Toaster } from 'sonner';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <BookmarkProvider>
          <App />
          <Toaster
            theme="dark"
            position="bottom-right"
            richColors
            toastOptions={{
              style: {
                background: '#0d0d10',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: '#e4e4e7',
                fontFamily: 'Inter, sans-serif',
                fontSize: '0.8125rem',
              },
            }}
          />
        </BookmarkProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
