const Sidebar = ({ onUpload }) => {
    return (
      <div className="sidebar board">
        <h3>Upload Video</h3>
        <input type="file" accept="video/mp4" onChange={(e) => onUpload(e.target.files[0])} />
      </div>
    );
  };
  
  export default Sidebar;
  