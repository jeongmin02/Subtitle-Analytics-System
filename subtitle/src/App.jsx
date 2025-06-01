import { useEffect, useMemo, useState } from 'react';
import TopBar from './components/TopBar';
import Sidebar from './components/Sidebar';
import VideoPlayer from './components/VideoPlayer';
import Dashboard from './components/Dashboard';
import resultData from './data/result2.json';
import analysisData from './data/analysis6_with_scores.json';
import './styles/layout.css';

const App = () => {
  const [videoDataList, setVideoDataList] = useState([]);
  const [selectedVideoIndex, setSelectedVideoIndex] = useState(null);
  const [currentSubtitleId, setCurrentSubtitleId] = useState(null);

  const [subtitles, setSubtitles] = useState(resultData);
  const [analysis, setAnalysis] = useState(analysisData);

  const generateThumbnail = (videoFile) => {
    return new Promise((resolve) => {
      const video = document.createElement('video');
      video.src = URL.createObjectURL(videoFile);
      video.crossOrigin = 'anonymous';
      video.muted = true;
      video.currentTime = 1;
      video.addEventListener('loadeddata', () => {
        const canvas = document.createElement('canvas');
        canvas.width = 160;
        canvas.height = 90;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const thumbnailUrl = canvas.toDataURL('image/jpeg');
        resolve(thumbnailUrl);
      });
    });
  };

  const handleUpload = async (files) => {
    const newFiles = Array.from(files);
    const newData = await Promise.all(
      newFiles.map(async (file) => {
        const thumbnail = await generateThumbnail(file);
        return { file, thumbnail };
      })
    );
    setVideoDataList((prev) => [...prev, ...newData]);
    if (selectedVideoIndex === null && newData.length > 0) {
      setSelectedVideoIndex(0);
    }
  };

  const parseTime = (str) => {
    const [hh, mm, ssMs] = str.split(':');
    const [ss, ms] = ssMs.split(',');
    return (
      Number(hh) * 3600 +
      Number(mm) * 60 +
      Number(ss) +
      Number(ms) / 1000
    );
  };

  const handleTimeUpdate = (currentTimeInSeconds) => {
    const matched = subtitles.find((s) => {
      const start = parseTime(s.start_time);
      const end = parseTime(s.end_time);
      return currentTimeInSeconds >= start && currentTimeInSeconds < end;
    });

    if (matched && matched.id !== currentSubtitleId) {
      setCurrentSubtitleId(matched.id);
    }
  };

  const videoUrl = useMemo(() => {
    if (selectedVideoIndex !== null && videoDataList[selectedVideoIndex]) {
      return URL.createObjectURL(videoDataList[selectedVideoIndex].file);
    }
    return null;
  }, [selectedVideoIndex, videoDataList]);

  const currentAnalysis = analysis.find((a) => a.id === currentSubtitleId);

  const highlightVideo =
    currentAnalysis?.composite_scores?.some((score) => score.composite_score >= 5.0) ?? false;

  return (
    <>
      <TopBar />
      <div className="main-layout">
        <Sidebar
          onUpload={handleUpload}
          videoDataList={videoDataList}
          onSelect={(index) => setSelectedVideoIndex(index)}
          selectedVideoIndex={selectedVideoIndex}
        />
        <VideoPlayer
          videoUrl={videoUrl}
          onTimeUpdate={handleTimeUpdate}
          highlight={highlightVideo}
        />
        <Dashboard analysis={currentAnalysis} />
      </div>
    </>
  );
};

export default App;
