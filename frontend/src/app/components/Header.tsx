'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { isAuthenticated, clearAuthState } from '../../lib/auth';

const Header: React.FC = () => {
  const router = useRouter();
  const [isClient, setIsClient] = useState(false);
  const [isAuthenticatedState, setIsAuthenticatedState] = useState(false);

  useEffect(() => {
    // Set isClient to true after component mounts (client-side only)
    setIsClient(true);
    // Update authentication state after mounting
    setIsAuthenticatedState(isAuthenticated());
  }, []);

  const handleLogout = () => {
    clearAuthState();
    router.push('/auth');
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center relative">
        
        {/* Left side: App Name */}
        <Link href="/" className="text-xl sm:text-2xl font-bold text-blue-600">
          Todo App
        </Link>

        {/* Plan Your Day */}
        {isClient && isAuthenticatedState && (
          <span className="
            text-base sm:text-2xl text-blue-800 font-bold
            absolute right-4 md:left-1/2 md:right-auto md:transform md:-translate-x-1/2
          ">
            📋 Plan Your Day 📝
          </span>
        )}
      </div>
    </header>
  );
};

export default Header;