const Dashboard = ({ analysis }) => {
    if (!analysis) {
      return (
        <div className="dashboard board">
          <h2 className="section-title">📊 Analysis Dashboard</h2>
          <p>No analysis available</p>
        </div>
      );
    }
  
    const emotions = Object.keys(analysis.white_subtitle_scores);
  
    return (
      <div className="dashboard board">
        <h2 className="section-title">📊 Analysis Dashboard</h2>
  
        {/* 1. 대사 자막 분석 */}
        <h4 className="section-title">🗣️ 대사 자막 감정 분석</h4>
        <ul className="text-analysis-list">
          {Object.entries(analysis.differences_explained).map(([emotion, desc]) => (
            <li key={emotion}>
              <strong>{emotion}:</strong> {desc}
            </li>
          ))}
        </ul>
  
        {/* 2. 대사 외 자막 분석 */}
        <h4 className="section-title">📝 대사 외 자막 감정 분석</h4>
        <ul className="text-analysis-list">
          {analysis.extra_emotional_effect_from_added_text.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
  
        {/* 3. 감정 점수 변화 시각화 */}
        <h4 className="score-title">감정 점수 변화</h4>
  
        {emotions.map((emotion) => {
          const before = analysis.white_subtitle_scores[emotion];
          const after = analysis.designed_subtitle_scores[emotion];
  
          const min = Math.min(before, after);
          const max = Math.max(before, after);
  
          return (
            <div key={emotion} className="emotion-bar">
              <span className="emotion-label">{emotion}</span>
              <div className="bar-container">
                {[1, 2, 3, 4, 5, 6, 7].map((val) => {
                  const isBetween = val > min && val < max;
                  return (
                    <div
                      key={val}
                      className={`bar-segment ${isBetween ? 'bar-fill' : ''}`}
                    >
                      {val === before && <div className="dot before" />}
                      {val === after && <div className="dot after" />}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    );
  };
  
  export default Dashboard;
  