import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { App } from './App';
import { AuthProvider } from '@/context/AuthContext';
import { BookmarkProvider } from '@/context/BookmarkContext';
import { ThemeProvider, useTheme } from '@/context/ThemeContext';
import { Toaster } from 'sonner';
import './index.css';

const AppShell: React.FC = () => {
  const { resolvedTheme } = useTheme();

  return (
    <>
      <App />
      <Toaster
        theme={resolvedTheme}
        position="bottom-right"
        richColors
      />
    </>
  );
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <BookmarkProvider>
            <AppShell />
          </BookmarkProvider>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);

