'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';

type User = {
  name: string;
  email: string;
};

type AuthContextType = {
  token: string | null;
  user: User | null;
  signin: (token: string, user: User) => void;
  signout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('breezi_token');
    const userStr = localStorage.getItem('breezi_user');
    if (stored) setToken(stored);
    if (userStr) setUser(JSON.parse(userStr));
  }, []);

  const signin = (value: string, nextUser: User) => {
    localStorage.setItem('breezi_token', value);
    localStorage.setItem('breezi_user', JSON.stringify(nextUser));
    setToken(value);
    setUser(nextUser);
  };

  const signout = () => {
    localStorage.removeItem('breezi_token');
    localStorage.removeItem('breezi_user');
    setToken(null);
    setUser(null);
  };

  const value = useMemo(() => ({ token, user, signin, signout }), [token, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
