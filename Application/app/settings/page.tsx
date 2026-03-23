'use client';

import { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import { User, Building, Bell } from 'lucide-react';

const tabs = [
  { id: 'account', label: 'Account', icon: User },
  { id: 'workspace', label: 'Workspace', icon: Building },
  { id: 'notifications', label: 'Notifications', icon: Bell },
];

export default function SettingsPage() {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState('account');
  
  // Form states
  const [accountForm, setAccountForm] = useState({
    firstName: user?.name?.split(' ')[0] || '',
    lastName: user?.name?.split(' ')[1] || '',
    email: user?.email || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
    timezone: 'America/New_York',
  });

  const [workspaceForm, setWorkspaceForm] = useState({
    companyName: 'Acme Corp',
    supportEmail: 'support@acmecorp.com',
    openingTime: '09:00',
    closingTime: '17:00',
  });

  const [notificationsForm, setNotificationsForm] = useState({
    dailySummary: true,
    criticalAlerts: true,
    leadSMS: false,
  });

  const handleAccountChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setAccountForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleWorkspaceChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setWorkspaceForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleNotificationsChange = (name: string) => {
    setNotificationsForm((prev) => ({ ...prev, [name]: !prev[name as keyof typeof prev] }));
  };

  const handleSaveChanges = (tabName: string) => {
    console.log(`Saving ${tabName} changes:`, {
      account: accountForm,
      workspace: workspaceForm,
      notifications: notificationsForm,
    }[tabName]);
  };

  return (
    <>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-gray-600">Manage your account, workspace, and preferences.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-4 lg:gap-8">
        {/* Left Sidebar - Tabs */}
        <div className="lg:col-span-1">
          <nav className="flex flex-row gap-2 overflow-x-auto lg:flex-col lg:gap-0 border-b lg:border-b-0 lg:border-l border-gray-200 lg:pr-6">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-3 whitespace-nowrap px-4 py-3 text-sm font-medium border-b-2 lg:border-b-0 lg:border-l-2 transition-colors ${
                    isActive
                      ? 'border-breezi-500 bg-orange-50 text-breezi-600 lg:border-l-2'
                      : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <IconComponent className="h-4 w-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Right Content Area */}
        <div className="lg:col-span-3">
          {/* ACCOUNT TAB */}
          {activeTab === 'account' && (
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Account Settings</h2>

              {/* Personal Information */}
              <div className="mb-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Personal Information</h3>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      First Name
                    </label>
                    <input
                      type="text"
                      name="firstName"
                      value={accountForm.firstName}
                      onChange={handleAccountChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                      placeholder="John"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Last Name
                    </label>
                    <input
                      type="text"
                      name="lastName"
                      value={accountForm.lastName}
                      onChange={handleAccountChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                      placeholder="Doe"
                    />
                  </div>
                </div>
              </div>

              {/* Email Address */}
              <div className="mb-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Email Address</h3>
                <input
                  type="email"
                  name="email"
                  value={accountForm.email}
                  onChange={handleAccountChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                  placeholder="john@example.com"
                />
              </div>

              {/* Change Password */}
              <div className="mb-8 pb-8 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Change Password</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Current Password
                    </label>
                    <input
                      type="password"
                      name="currentPassword"
                      value={accountForm.currentPassword}
                      onChange={handleAccountChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                      placeholder="••••••••"
                    />
                  </div>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        New Password
                      </label>
                      <input
                        type="password"
                        name="newPassword"
                        value={accountForm.newPassword}
                        onChange={handleAccountChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                        placeholder="••••••••"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Confirm Password
                      </label>
                      <input
                        type="password"
                        name="confirmPassword"
                        value={accountForm.confirmPassword}
                        onChange={handleAccountChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                        placeholder="••••••••"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Timezone */}
              <div className="mb-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Preferences</h3>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Timezone
                  </label>
                  <select
                    name="timezone"
                    value={accountForm.timezone}
                    onChange={handleAccountChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                  >
                    <option value="America/New_York">Eastern Time (ET)</option>
                    <option value="America/Chicago">Central Time (CT)</option>
                    <option value="America/Denver">Mountain Time (MT)</option>
                    <option value="America/Los_Angeles">Pacific Time (PT)</option>
                    <option value="Europe/London">GMT / London</option>
                    <option value="Europe/Paris">Central European Time (CET)</option>
                    <option value="Asia/Tokyo">Japan Standard Time (JST)</option>
                  </select>
                </div>
              </div>

              <button
                onClick={() => handleSaveChanges('account')}
                className="px-6 py-2 bg-breezi-600 text-white rounded-lg hover:bg-breezi-700 transition-colors font-medium"
              >
                Save Changes
              </button>
            </div>
          )}

          {/* WORKSPACE TAB */}
          {activeTab === 'workspace' && (
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Workspace Settings</h2>

              {/* Business Profile */}
              <div className="mb-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Business Profile</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Company Name
                    </label>
                    <input
                      type="text"
                      name="companyName"
                      value={workspaceForm.companyName}
                      onChange={handleWorkspaceChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                      placeholder="Acme Corp"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Support Email
                    </label>
                    <input
                      type="email"
                      name="supportEmail"
                      value={workspaceForm.supportEmail}
                      onChange={handleWorkspaceChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                      placeholder="support@company.com"
                    />
                  </div>
                </div>
              </div>

              {/* Business Hours */}
              <div className="mb-8">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Business Hours</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Set the hours when Breezi AI will process and take calls.
                </p>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Opening Time
                    </label>
                    <input
                      type="time"
                      name="openingTime"
                      value={workspaceForm.openingTime}
                      onChange={handleWorkspaceChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Closing Time
                    </label>
                    <input
                      type="time"
                      name="closingTime"
                      value={workspaceForm.closingTime}
                      onChange={handleWorkspaceChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-breezi-500 focus:border-transparent outline-none transition"
                    />
                  </div>
                </div>
              </div>

              <button
                onClick={() => handleSaveChanges('workspace')}
                className="px-6 py-2 bg-breezi-600 text-white rounded-lg hover:bg-breezi-700 transition-colors font-medium"
              >
                Save Changes
              </button>
            </div>
          )}

          {/* NOTIFICATIONS TAB */}
          {activeTab === 'notifications' && (
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Notification Preferences</h2>

              <div className="space-y-4">
                {/* Daily Summary */}
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                  <div>
                    <p className="font-medium text-gray-900">Daily Summary Emails</p>
                    <p className="text-sm text-gray-600">Get a daily digest of your call activity</p>
                  </div>
                  <button
                    onClick={() => handleNotificationsChange('dailySummary')}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      notificationsForm.dailySummary ? 'bg-breezi-600' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        notificationsForm.dailySummary ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                {/* Critical Alerts */}
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                  <div>
                    <p className="font-medium text-gray-900">Critical AI Alerts</p>
                    <p className="text-sm text-gray-600">Receive alerts when something goes wrong</p>
                  </div>
                  <button
                    onClick={() => handleNotificationsChange('criticalAlerts')}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      notificationsForm.criticalAlerts ? 'bg-breezi-600' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        notificationsForm.criticalAlerts ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                {/* Lead SMS Notifications */}
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
                  <div>
                    <p className="font-medium text-gray-900">New Lead SMS Notifications</p>
                    <p className="text-sm text-gray-600">Get SMS alerts for new qualified leads</p>
                  </div>
                  <button
                    onClick={() => handleNotificationsChange('leadSMS')}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      notificationsForm.leadSMS ? 'bg-breezi-600' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        notificationsForm.leadSMS ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              </div>

              <div className="mt-8 pt-8 border-t border-gray-200">
                <button
                  onClick={() => handleSaveChanges('notifications')}
                  className="px-6 py-2 bg-breezi-600 text-white rounded-lg hover:bg-breezi-700 transition-colors font-medium"
                >
                  Save Changes
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
