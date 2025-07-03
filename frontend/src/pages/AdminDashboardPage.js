import React, { useState } from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import { FaUsers, FaBoxOpen, FaClipboardList, FaTags, FaChartBar } from 'react-icons/fa';

// Import admin sub-pages
import AdminDashboardHome from '../components/admin/AdminDashboardHome';
import AdminProducts from '../components/admin/AdminProducts';
import AdminCategories from '../components/admin/AdminCategories';
import AdminUsers from '../components/admin/AdminUsers';
import AdminOrders from '../components/admin/AdminOrders';

const AdminDashboardPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/admin', icon: <FaChartBar className="mr-2" />, text: 'Dashboard', component: <AdminDashboardHome /> },
    { path: '/admin/products', icon: <FaBoxOpen className="mr-2" />, text: 'Products', component: <AdminProducts /> },
    { path: '/admin/categories', icon: <FaTags className="mr-2" />, text: 'Categories', component: <AdminCategories /> },
    { path: '/admin/orders', icon: <FaClipboardList className="mr-2" />, text: 'Orders', component: <AdminOrders /> },
    { path: '/admin/users', icon: <FaUsers className="mr-2" />, text: 'Users', component: <AdminUsers /> },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-8">Admin Dashboard</h1>
      
      {/* Mobile Nav Toggle */}
      <div className="md:hidden mb-4">
        <button
          onClick={() => setShowMobileMenu(!showMobileMenu)}
          className="w-full bg-gray-100 px-4 py-2 rounded-md text-left flex justify-between items-center"
        >
          <span>Admin Menu</span>
          <span>{showMobileMenu ? '▲' : '▼'}</span>
        </button>
      </div>
      
      <div className="flex flex-col md:flex-row gap-8">
        {/* Sidebar Navigation */}
        <nav className={`md:w-64 flex-shrink-0 ${showMobileMenu ? 'block' : 'hidden'} md:block`}>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <ul>
              {navItems.map((item, index) => (
                <li key={index}>
                  <Link
                    to={item.path}
                    className={`flex items-center px-4 py-3 border-l-4 ${
                      isActive(item.path) 
                        ? 'bg-blue-50 border-blue-600 text-blue-600' 
                        : 'border-transparent hover:bg-gray-50'
                    }`}
                  >
                    {item.icon}
                    {item.text}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </nav>
        
        {/* Main Content */}
        <div className="flex-grow bg-white rounded-lg shadow p-6">
          <Routes>
            <Route index element={<AdminDashboardHome />} />
            <Route path="products" element={<AdminProducts />} />
            <Route path="categories" element={<AdminCategories />} />
            <Route path="orders" element={<AdminOrders />} />
            <Route path="users" element={<AdminUsers />} />
          </Routes>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardPage;
