const VideoPlayer = ({ videoUrl }) => {
    return (
      <div className="video-player board">
        {videoUrl ? (
          <video src={videoUrl} controls width="100%" />
        ) : (
          <p>No video selected</p>
        )}
      </div>
    );
  };
  
  export default VideoPlayer;
  