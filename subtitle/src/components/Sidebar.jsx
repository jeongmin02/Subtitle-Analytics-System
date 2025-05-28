const Sidebar = ({ onUpload, videoDataList, onSelect, selectedVideoIndex }) => {
    return (
      <div className="sidebar board">
        <h2 className="section-title">📁 Video Upload & List</h2>
        <div className="sidebar-inner">
          <div className="upload-section">
            <input
              type="file"
              accept="video/mp4"
              multiple
              onChange={(e) => onUpload(e.target.files)}
            />
          </div>
  
          {/* <hr className="divider" /> */}
  
          <div className="thumbnail-section">
            <h4>Uploaded Videos</h4>
            <div className="video-thumbnails">
              {videoDataList.map((data, index) => (
                <div
                  key={index}
                  className={`video-thumb ${index === selectedVideoIndex ? 'selected' : ''}`}
                  onClick={() => onSelect(index)}
                >
                  <img src={data.thumbnail} alt="thumbnail" className="thumb-img" />
                  <div className="thumb-name">{data.file.name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };
  
export default Sidebar;
