import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import TeacherDashboard from './pages/TeacherDashboard';
import TeacherMonitor from './pages/TeacherMonitor';
import StudentSession from './pages/StudentSession';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/teacher" element={<TeacherDashboard />} />
          <Route path="/monitor/:code" element={<TeacherMonitor />} />
          <Route path="/session/:code" element={<StudentSession />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
