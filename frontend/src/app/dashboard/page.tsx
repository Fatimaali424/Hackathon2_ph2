'use client';

import React, { useState, useEffect } from 'react';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';
import { isAuthenticated, clearAuthState } from '../../lib/auth';
import { useRouter } from 'next/navigation';

const DashboardPage = () => {
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [taskCount, setTaskCount] = useState(0);
  const [isClient, setIsClient] = useState(false);
  const router = useRouter();

  const handleLogout = () => {
    clearAuthState();
    router.push('/auth');
  };

  // Check if user is authenticated only on client side
  useEffect(() => {
    setIsClient(true);
    if (!isAuthenticated()) {
      window.location.href = '/auth';
    }
  }, []);

  // Don't render anything until client-side check is complete
  if (!isClient) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If client-side check reveals user is not authenticated,
  // the redirect above will have already happened
  // but we include a fallback render just in case
  if (!isAuthenticated()) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <span className="text-xl font-bold text-gray-900">Todo Dashboard</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-2xl font-bold text-blue-700 ">
                Welcome back!
              </span>
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-red-500 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all duration-200 hover:scale-105"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Manage Your Tasks</h1>
            <p className="text-gray-600">
              You have <span className="font-semibold text-blue-600">{taskCount}</span> task
              {taskCount !== 1 ? 's' : ''} in your list
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left column - Task Form */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-lg p-6 sticky top-6 border border-gray-100">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">Create New Task</h2>
                  {showTaskForm && (
                    <button
                      onClick={() => setShowTaskForm(false)}
                      className="text-gray-500 hover:text-gray-700 transition-colors duration-200"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  )}
                </div>

                {!showTaskForm ? (
                  <button
                    onClick={() => setShowTaskForm(true)}
                    className="w-full py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 hover:scale-[1.02]"
                  >
                    <div className="flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      Add New Task
                    </div>
                  </button>
                ) : (
                  <TaskForm
                    onTaskCreated={() => {
                      setShowTaskForm(false);
                    }}
                    onCancel={() => setShowTaskForm(false)}
                  />
                )}
              </div>
            </div>

            {/* Right column - Task List */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100">
                <div className="px-6 py-5 border-b border-gray-200 bg-gray-50">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>
                  </div>
                </div>
                <div className="p-6">
                  <TaskList onTaskCountChange={setTaskCount} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;