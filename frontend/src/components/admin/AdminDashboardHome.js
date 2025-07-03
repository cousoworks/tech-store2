import React from 'react';

const AdminDashboardHome = () => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-6">Dashboard Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-100 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-blue-800">Total Products</h3>
          <p className="text-2xl font-bold">0</p>
        </div>
        <div className="bg-green-100 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-green-800">Total Orders</h3>
          <p className="text-2xl font-bold">0</p>
        </div>
        <div className="bg-yellow-100 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-yellow-800">Total Users</h3>
          <p className="text-2xl font-bold">0</p>
        </div>
        <div className="bg-purple-100 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-purple-800">Total Revenue</h3>
          <p className="text-2xl font-bold">$0.00</p>
        </div>
      </div>
      
      <div className="bg-gray-100 p-4 rounded-lg">
        <h3 className="text-lg font-medium mb-2">Recent Activity</h3>
        <p className="text-gray-500">No recent activity</p>
      </div>
    </div>
  );
};

export default AdminDashboardHome;
