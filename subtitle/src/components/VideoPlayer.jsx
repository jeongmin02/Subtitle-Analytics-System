const VideoPlayer = ({ videoUrl, onTimeUpdate, highlight }) => {
  const handleTimeUpdate = (e) => {
    const currentTime = e.target.currentTime;
    if (onTimeUpdate) {
      onTimeUpdate(currentTime);
    }
  };

  return (
    <div className="video-player board">
      <h2 className="section-title">🎬 Video Player</h2>
      {videoUrl ? (
        <div className="video-wrapper">
          <video
            src={videoUrl}
            controls
            width="100%"
            onTimeUpdate={handleTimeUpdate}
            className={`video-element ${highlight ? 'highlight-border' : ''}`}
          />
        </div>
      
      ) : (
        <p>No video selected</p>
      )}
    </div>
  );
};

export default VideoPlayer;
