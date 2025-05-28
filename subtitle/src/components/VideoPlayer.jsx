const VideoPlayer = ({ videoUrl, onTimeUpdate }) => {
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
        <video
          src={videoUrl}
          controls
          width="100%"
          onTimeUpdate={handleTimeUpdate}
        />
      ) : (
        <p>No video selected</p>
      )}
    </div>
  );
};

export default VideoPlayer;
