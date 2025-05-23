const Dashboard = ({ analysis }) => {
    return (
      <div className="dashboard board">
        <h3>Analysis</h3>
        {analysis ? (
          <pre>{JSON.stringify(analysis, null, 2)}</pre>
        ) : (
          <p>No analysis available</p>
        )}
      </div>
    );
  };
  
  export default Dashboard;
  