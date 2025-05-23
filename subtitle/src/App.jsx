// pages/App.jsx
import { useState } from 'react';
import TopBar from './components/TopBar';
import Sidebar from './components/Sidebar';
import VideoPlayer from './components/VideoPlayer';
import Dashboard from './components/Dashboard';
import './styles/layout.css';

const App = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const handleUpload = (file) => {
    setVideoFile(file);
    setVideoUrl(URL.createObjectURL(file));
    setAnalysis(null); // 초기화
    // 추후: API로 분석 요청 가능
  };

  return (
    <>
      <TopBar />
      <div className="main-layout">
        <Sidebar onUpload={handleUpload} />
        <VideoPlayer videoUrl={videoUrl} />
        <Dashboard analysis={analysis} />
      </div>
    </>
  );
};

export default App;
