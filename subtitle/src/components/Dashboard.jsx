const Dashboard = ({ analysis }) => {
  if (!analysis) {
    return (
      <div className="dashboard board">
        <h2 className="section-title">📊 Analysis Dashboard</h2>
        <p>No analysis available</p>
      </div>
    );
  }

  const emotionScores = analysis.emotion_scores || [];
  const subtitleAnalysis = analysis.emotion_analysis?.["대사 자막"] || {};
  const nonSubtitleAnalysis = analysis.emotion_analysis?.["대사 외 자막"] || [];

  return (
    <div className="dashboard board">
      <h2 className="section-title">📊 Analysis Dashboard</h2>

      {/* 1. 대사 자막 감정 분석 */}
      <section className="dashboard-section">
        <h4 className="section-title">🗣️ 대사 자막 감정 분석</h4>
        {Object.keys(subtitleAnalysis).length > 0 ? (
          <ul className="text-analysis-list">
            {Object.entries(subtitleAnalysis).map(([emotion, desc]) => (
              <li key={emotion}>
                <strong>{emotion.replace(/"/g, '')}:</strong> {desc}
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-data">분석 데이터가 없습니다.</p>
        )}
      </section>

      {/* 2. 대사 외 자막 감정 분석 */}
      <section className="dashboard-section">
        <h4 className="section-title">💬 대사 외 자막 감정 분석</h4>
        {nonSubtitleAnalysis.length > 0 ? (
          <ul className="text-analysis-list">
            {nonSubtitleAnalysis.map((text, idx) => (
              <li key={idx}>{text}</li>
            ))}
          </ul>
        ) : (
          <p className="no-data">분석 데이터가 없습니다.</p>
        )}
      </section>

      {/* 3. 감정 점수 변화 시각화 */}
      <section className="dashboard-section">
        <h4 className="section-title">🎯 자막 디자인에 의한 감정 변화</h4>
        {emotionScores.length > 0 ? (
          emotionScores.map(({ emotion, before_score, after_score }) => {
            const min = Math.min(before_score, after_score);
            const max = Math.max(before_score, after_score);
            return (
              <div key={emotion} className="emotion-bar">
              <span className="emotion-label">{emotion}</span>
              <div className="bar-wrapper">
                <div className="bar-container">
                  {[1, 2, 3, 4, 5, 6, 7].map((val) => {
                    const isBetween = val > min && val < max;
                    return (
                      <div
                        key={val}
                        className={`bar-segment ${isBetween ? 'bar-fill' : ''}`}
                      >
                        {val === before_score && <div className="dot before" />}
                        {val === after_score && <div className="dot after" />}
                      </div>
                    );
                  })}
                </div>
                <div className="bar-labels">
                  {[1, 2, 3, 4, 5, 6, 7].map((val) => (
                    <span key={val} className="bar-label">{val}</span>
                  ))}
                </div>
              </div>
            </div>
            );
          })
        ) : (
          <p className="no-data">점수 변화 데이터가 없습니다.</p>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
