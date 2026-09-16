import {
  useEffect,
  useState,
} from "react";

const API_BASE =
  "http://127.0.0.1:8010";

function RiskAlerts({
  currentPrediction,
}) {
  const [alerts, setAlerts] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  /* =====================================================
     OLD ALERTS
  ===================================================== */

  const loadAlerts = async () => {
    try {
      setLoading(true);
      setError("");

      const response =
        await fetch(
          `${API_BASE}/api/top-risk?limit=10`
        );

      if (!response.ok) {
        throw new Error(
          `API returned ${response.status}`
        );
      }

      const result =
        await response.json();

      if (
        result.status !==
        "success"
      ) {
        throw new Error(
          result.message ||
            "Unable to load alerts"
        );
      }

      const alertData =
        (result.data || [])
          .filter(
            (item) =>
              item.risk_level ===
                "High" ||
              item.risk_level ===
                "Very High"
          );

      setAlerts(
        alertData
      );
    } catch (err) {
      console.error(
        "Risk alerts error:",
        err
      );

      setError(
        "Unable to load risk alerts."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =====================================================
     INITIAL
  ===================================================== */

  useEffect(() => {
    if (!currentPrediction) {
      loadAlerts();
    }
  }, [currentPrediction]);

  /* =====================================================
     CURRENT UPLOAD
  ===================================================== */

  useEffect(() => {
    if (currentPrediction) {
      if (
        currentPrediction.risk_level ===
          "High" ||
        currentPrediction.risk_level ===
          "Very High"
      ) {
        setAlerts([
          currentPrediction,
        ]);
      } else {
        setAlerts([]);
      }

      setLoading(false);
      setError("");
    }
  }, [currentPrediction]);

  const veryHighCount =
    alerts.filter(
      (item) =>
        item.risk_level ===
        "Very High"
    ).length;

  const highCount =
    alerts.filter(
      (item) =>
        item.risk_level ===
        "High"
    ).length;

  return (
    <section className="predictionPanel">

      <div className="predictionHeader">

        <div>
          <h2>
            Risk Alerts
          </h2>

          <p>
            {currentPrediction
              ? "Alert generated from the latest uploaded satellite image"
              : "Priority areas requiring monitoring and review"}
          </p>
        </div>

        <button
          className="refreshButton"
          onClick={() => {
            if (
              currentPrediction
            ) {
              if (
                currentPrediction.risk_level ===
                  "High" ||
                currentPrediction.risk_level ===
                  "Very High"
              ) {
                setAlerts([
                  currentPrediction,
                ]);
              } else {
                setAlerts([]);
              }
            } else {
              loadAlerts();
            }
          }}
        >
          ↻ Refresh
        </button>
      </div>

      <div className="analyticsSummaryGrid">

        <div className="analyticsStatCard redStat">
          <span>
            VERY HIGH
          </span>

          <strong>
            {veryHighCount}
          </strong>
        </div>

        <div className="analyticsStatCard orangeStat">
          <span>
            HIGH
          </span>

          <strong>
            {highCount}
          </strong>
        </div>

        <div className="analyticsStatCard blueStat">
          <span>
            TOTAL ALERTS
          </span>

          <strong>
            {alerts.length}
          </strong>
        </div>

        <div className="analyticsStatCard greenStat">
          <span>
            STATUS
          </span>

          <strong>
            Active
          </strong>
        </div>
      </div>

      {loading && (
        <div className="predictionLoading">
          Loading risk alerts...
        </div>
      )}

      {error && (
        <div className="predictionError">
          ⚠️ {error}
        </div>
      )}

      {!loading &&
        !error &&
        alerts.length === 0 && (
          <div
            className="card panel"
            style={{
              marginTop: "20px",
            }}
          >
            <div className="infoBox">

              <div className="infoIcon">
                ✅
              </div>

              <p>
                No High or Very High risk
                alerts are currently generated
                for the selected prediction.
              </p>
            </div>
          </div>
        )}

      {!loading &&
        !error &&
        alerts.length > 0 && (
          <div
            style={{
              display: "grid",
              gap: "14px",
              marginTop: "20px",
            }}
          >
            {alerts.map(
              (item) => (
                <div
                  className="card panel"
                  key={`${item.image}-${item.risk_score}`}
                >
                  <div
                    style={{
                      display:
                        "flex",
                      justifyContent:
                        "space-between",
                      alignItems:
                        "center",
                      gap: "16px",
                      flexWrap:
                        "wrap",
                    }}
                  >
                    <div>

                      <h3>
                        🚨 {item.image}
                      </h3>

                      <p>
                        Preliminary AI
                        risk alert
                      </p>
                    </div>

                    <span
                      className={`riskBadge ${
                        item.risk_level ===
                        "Very High"
                          ? "riskVeryHigh"
                          : "riskHigh"
                      }`}
                    >
                      {
                        item.risk_level
                      }
                    </span>
                  </div>

                  <div className="predictionMetrics">

                    <div>
                      <span>
                        Risk Score
                      </span>

                      <strong>
                        {item.risk_score.toFixed(
                          2
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>
                        Predicted Area
                      </span>

                      <strong>
                        {item
                          .predicted_area_percent
                          .toFixed(
                            2
                          )}
                        %
                      </strong>
                    </div>

                    <div>
                      <span>
                        Mean Probability
                      </span>

                      <strong>
                        {(
                          item
                            .mean_probability *
                          100
                        ).toFixed(
                          2
                        )}
                        %
                      </strong>
                    </div>

                    <div>
                      <span>
                        Max Probability
                      </span>

                      <strong>
                        {(
                          item
                            .max_probability *
                          100
                        ).toFixed(
                          2
                        )}
                        %
                      </strong>
                    </div>
                  </div>
                </div>
              )
            )}
          </div>
        )}
    </section>
  );
}

export default RiskAlerts;