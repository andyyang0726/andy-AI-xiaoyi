import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import EnterpriseList from './pages/EnterpriseList';
import DemandList from './pages/DemandList';
import DemandCreate from './pages/DemandCreate';
import DemandDetail from './pages/DemandDetail';
import RecommendedDemands from './pages/RecommendedDemands';
import SupplierHome from './pages/SupplierHome';
import SupplierRegister from './pages/SupplierRegister';
import DemandQualification from './pages/DemandQualification';
import MatchedSuppliers from './pages/MatchedSuppliers';
import MatchedClients from './pages/MatchedClients';
import Profile from './pages/Profile';
import './App.css';

// 私有路由组件
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
};

function App() {
  // HashRouter 不需要 basename，直接使用 hash 路由
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout />
              </PrivateRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="profile" element={<Profile />} />
            <Route path="enterprises" element={<EnterpriseList />} />
            <Route path="demands" element={<DemandList />} />
            <Route path="demands/create" element={<DemandCreate />} />
            <Route path="demands/:id" element={<DemandDetail />} />
            <Route path="recommended" element={<RecommendedDemands />} />
            <Route path="supplier-home" element={<SupplierHome />} />
            <Route path="supplier-register" element={<SupplierRegister />} />
            <Route path="qualification" element={<DemandQualification />} />
            <Route path="matched-suppliers" element={<MatchedSuppliers />} />
            <Route path="matched-clients" element={<MatchedClients />} />
          </Route>
        </Routes>
      </Router>
    </ConfigProvider>
  );
}

export default App;
