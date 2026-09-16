import { useEffect, useState } from "react";
import "./App.css";
import Predictions from "./Predictions";
import RiskAlerts from "./RiskAlerts";

const API_BASE = "http://127.0.0.1:8010";

/* =========================================================
   RISK BAR
========================================================= */

function RiskBar({
  label,
  value,
  total,
  className,
}) {
  const percentage =
    total > 0 ? (value / total) * 100 : 0;

  return (
    <div className="riskBar">
      <div className="riskTop">
        <span>{label}</span>
        <strong>{value}</strong>
      </div>

      <div className="barBackground">
        <div
          className={`barFill ${className}`}
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>

      <small
        style={{
          display: "block",
          marginTop: "4px",
          color: "#718097",
          fontSize: "10px",
        }}
      >
        {percentage.toFixed(1)}% of predictions
      </small>
    </div>
  );
}

/* =========================================================
   PRECAUTIONS
========================================================= */

function getPrecautions(riskLevel) {
  switch (riskLevel) {
    case "Low":
      return [
        "Continue routine monitoring of the identified area.",
        "Keep track of local rainfall and ground conditions.",
        "Review new AI predictions when available.",
      ];

    case "Moderate":
      return [
        "Increase monitoring frequency of the identified area.",
        "Check recent rainfall and local ground conditions.",
        "Consider field verification by qualified personnel.",
        "Follow relevant local advisory information.",
      ];

    case "High":
      return [
        "Prioritize the area for detailed review.",
        "Arrange field verification by qualified personnel.",
        "Monitor rainfall, drainage, cracks, and other visible ground changes.",
        "Check official local warnings and instructions.",
      ];

    case "Very High":
      return [
        "Prioritize immediate expert review of the identified area.",
        "Arrange field verification by qualified personnel.",
        "Closely monitor rainfall, drainage, and visible ground changes.",
        "Follow official alerts and instructions from local authorities.",
        "Restrict access to potentially affected locations when advised by authorities.",
      ];

    default:
      return [
        "Continue monitoring and verify the AI result with relevant local information.",
      ];
  }
}

/* =========================================================
   BUILD DASHBOARD FROM UPLOADED PREDICTION
========================================================= */

function buildDashboardFromPrediction(result) {
  const prediction = result?.prediction;

  if (!prediction) {
    return null;
  }

  const risk = prediction.risk_level;

  return {
    total_images: 1,

    low: risk === "Low" ? 1 : 0,

    moderate:
      risk === "Moderate" ? 1 : 0,

    high:
      risk === "High" ? 1 : 0,

    very_high:
      risk === "Very High" ? 1 : 0,

    average_risk_score:
      prediction.risk_score,

    maximum_risk_score:
      prediction.risk_score,
  };
}

/* =========================================================
   ANALYTICS
========================================================= */

function AnalyticsCards({ data }) {
  const total = data?.total_images ?? 0;
  const low = data?.low ?? 0;
  const moderate = data?.moderate ?? 0;
  const high = data?.high ?? 0;
  const veryHigh = data?.very_high ?? 0;

  const highRiskTotal =
    high + veryHigh;

  const highRiskPercentage =
    total > 0
      ? ((highRiskTotal / total) * 100).toFixed(1)
      : "0.0";

  const safePercentage =
    total > 0
      ? (((low + moderate) / total) * 100).toFixed(1)
      : "0.0";

  return (
    <section className="analyticsDashboard">
      <div className="analyticsIntro">
        <div>
          <span className="eyebrow">
            AI ANALYTICS
          </span>

          <h2>
            Risk Intelligence Overview
          </h2>

          <p>
            Simple visual summary of current
            LandslideAI prediction results.
          </p>
        </div>
      </div>

      <div className="analyticsSummaryGrid">
        <div className="analyticsStatCard blueStat">
          <span>Total Predictions</span>

          <strong>{total}</strong>

          <small>
            Images analyzed by the AI pipeline
          </small>
        </div>

        <div className="analyticsStatCard greenStat">
          <span>Low + Moderate</span>

          <strong>
            {safePercentage}%
          </strong>

          <small>
            Predictions outside the high-risk group
          </small>
        </div>

        <div className="analyticsStatCard orangeStat">
          <span>High + Very High</span>

          <strong>
            {highRiskPercentage}%
          </strong>

          <small>
            Priority predictions requiring review
          </small>
        </div>

        <div className="analyticsStatCard redStat">
          <span>Very High</span>

          <strong>{veryHigh}</strong>

          <small>
            Highest-risk prediction tiles
          </small>
        </div>
      </div>

      <div className="analyticsVisualGrid">
        <div className="card analyticsBigCard">
          <div className="analyticsCardHeader">
            <div>
              <h3>Risk Distribution</h3>

              <p>
                Number of predictions in each risk category
              </p>
            </div>

            <span className="smallBadge">
              Live
            </span>
          </div>

          <RiskBar
            label="Low Risk"
            value={low}
            total={total}
            className="green"
          />

          <RiskBar
            label="Moderate Risk"
            value={moderate}
            total={total}
            className="yellow"
          />

          <RiskBar
            label="High Risk"
            value={high}
            total={total}
            className="orange"
          />

          <RiskBar
            label="Very High Risk"
            value={veryHigh}
            total={total}
            className="red"
          />
        </div>

        <div className="card analyticsBigCard">
          <div className="analyticsCardHeader">
            <div>
              <h3>
                Risk Score Overview
              </h3>

              <p>
                AI-derived average and maximum score
              </p>
            </div>

            <span className="smallBadge">
              Score
            </span>
          </div>

          <div className="scoreCompare">
            <div className="scoreMetric">
              <div className="scoreMetricTop">
                <span>
                  Average Risk
                </span>

                <strong>
                  {data?.average_risk_score?.toFixed(
                    2
                  ) ?? "0.00"}
                </strong>
              </div>

              <div className="scoreTrack">
                <div
                  className="scoreFill averageScore"
                  style={{
                    width: `${Math.min(
                      data?.average_risk_score ?? 0,
                      100
                    )}%`,
                  }}
                />
              </div>
            </div>

            <div className="scoreMetric">
              <div className="scoreMetricTop">
                <span>
                  Maximum Risk
                </span>

                <strong>
                  {data?.maximum_risk_score?.toFixed(
                    2
                  ) ?? "0.00"}
                </strong>
              </div>

              <div className="scoreTrack">
                <div
                  className="scoreFill maximumScore"
                  style={{
                    width: `${Math.min(
                      data?.maximum_risk_score ?? 0,
                      100
                    )}%`,
                  }}
                />
              </div>
            </div>
          </div>

          <div className="scoreExplanation">
            <div className="explanationIcon">
              🧠
            </div>

            <div>
              <strong>
                What does this mean?
              </strong>

              <p>
                A higher risk score indicates
                a stronger preliminary landslide
                signal from the AI prediction
                pipeline.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="card analyticsSummaryPanel">
        <div className="analyticsCardHeader">
          <div>
            <h3>
              Operational Summary
            </h3>

            <p>
              Quick interpretation for monitoring
            </p>
          </div>
        </div>

        <div className="operationGrid">
          <div className="operationItem">
            <div className="operationIcon greenIcon">
              ✓
            </div>

            <div>
              <strong>{low}</strong>

              <span>
                Low-risk predictions
              </span>
            </div>
          </div>

          <div className="operationItem">
            <div className="operationIcon yellowIcon">
              !
            </div>

            <div>
              <strong>{moderate}</strong>

              <span>
                Moderate-risk predictions
              </span>
            </div>
          </div>

          <div className="operationItem">
            <div className="operationIcon orangeIcon">
              ⚠
            </div>

            <div>
              <strong>{high}</strong>

              <span>
                High-risk predictions
              </span>
            </div>
          </div>

          <div className="operationItem">
            <div className="operationIcon redIcon">
              🚨
            </div>

            <div>
              <strong>{veryHigh}</strong>

              <span>
                Very-high-risk predictions
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* =========================================================
   APP
========================================================= */

function App() {
  const [data, setData] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [activeSection, setActiveSection] =
    useState("dashboard");

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [uploading, setUploading] =
    useState(false);

  const [uploadResult, setUploadResult] =
    useState(null);

  const [uploadError, setUploadError] =
    useState("");

  const [currentPrediction, setCurrentPrediction] =
    useState(null);

  /* =======================================================
     LOAD INITIAL DASHBOARD
  ======================================================= */

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_BASE}/api/risk-summary`
      );

      if (!response.ok) {
        throw new Error(
          `API returned ${response.status}`
        );
      }

      const result =
        await response.json();

      setData(result);
    } catch (err) {
      console.error(
        "Dashboard API error:",
        err
      );

      setError(
        "Unable to connect to LandslideAI API."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  /* =======================================================
     NAVIGATION
  ======================================================= */

  const goToSection = (sectionId) => {
    setActiveSection(sectionId);

    const element =
      document.getElementById(sectionId);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  /* =======================================================
     FILE SELECTION
  ======================================================= */

  const handleFileChange = (event) => {
    const file =
      event.target.files?.[0];

    setUploadResult(null);
    setUploadError("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    if (
      !file.name
        .toLowerCase()
        .endsWith(".h5")
    ) {
      setSelectedFile(null);

      setUploadError(
        "Please select a valid .h5 satellite image."
      );

      event.target.value = "";

      return;
    }

    setSelectedFile(file);
  };

  /* =======================================================
     UPLOAD + PREDICTION
  ======================================================= */

  const handlePredictUpload =
    async () => {
      if (!selectedFile) {
        setUploadError(
          "Please select a .h5 file first."
        );

        return;
      }

      try {
        setUploading(true);
        setUploadError("");
        setUploadResult(null);

        const formData =
          new FormData();

        formData.append(
          "file",
          selectedFile
        );

        const response =
          await fetch(
            `${API_BASE}/api/predict`,
            {
              method: "POST",
              body: formData,
            }
          );

        const result =
          await response.json();

        if (!response.ok) {
          throw new Error(
            result?.message ||
              `API returned ${response.status}`
          );
        }

        if (
          result.status !==
          "success"
        ) {
          throw new Error(
            result?.message ||
              "Prediction failed."
          );
        }

        setUploadResult(result);

        const predictionRecord = {
          image:
            result.filename.replace(
              /\.h5$/i,
              ""
            ),

          filename:
            result.filename,

          predicted_area_percent:
            result.prediction
              .predicted_area_percent,

          mean_probability:
            result.prediction
              .mean_probability,

          max_probability:
            result.prediction
              .max_probability,

          risk_score:
            result.prediction
              .risk_score,

          risk_level:
            result.prediction
              .risk_level,

          input_shape:
            result.input_shape,

          prediction_id:
            result.prediction_id,
        };

        setCurrentPrediction(
          predictionRecord
        );

        setData(
          buildDashboardFromPrediction(
            result
          )
        );
      } catch (err) {
        console.error(
          "Upload prediction error:",
          err
        );

        setUploadError(
          err.message ||
            "Unable to process the uploaded image."
        );
      } finally {
        setUploading(false);
      }
    };

  /* =======================================================
     CURRENT DASHBOARD VALUES
  ======================================================= */

  const total =
    data?.total_images ?? 0;

  const averageRisk =
    data?.average_risk_score ?? 0;

  const maximumRisk =
    data?.maximum_risk_score ?? 0;

  const highRisk =
    (data?.high ?? 0) +
    (data?.very_high ?? 0);

  const userPrediction =
    uploadResult?.prediction;

  return (
    <div className="app">

      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brandIcon">
            ⛰️
          </div>

          <div>
            <h1>
              LandslideAI
            </h1>

            <p>
              Risk Monitoring
            </p>
          </div>
        </div>

        <div className="sectionTitle">
          MONITORING
        </div>

        <button
          className={`navItem ${
            activeSection === "dashboard"
              ? "active"
              : ""
          }`}
          onClick={() =>
            goToSection("dashboard")
          }
        >
          <span>▦</span>
          Dashboard
        </button>

        <button
          className={`navItem ${
            activeSection === "ai-predictions"
              ? "active"
              : ""
          }`}
          onClick={() =>
            goToSection(
              "ai-predictions"
            )
          }
        >
          <span>◉</span>
          AI Predictions
        </button>

        <button
          className={`navItem ${
            activeSection === "risk-alerts"
              ? "active"
              : ""
          }`}
          onClick={() =>
            goToSection(
              "risk-alerts"
            )
          }
        >
          <span>⚠</span>
          Risk Alerts
        </button>

        <button
          className={`navItem ${
            activeSection === "analytics"
              ? "active"
              : ""
          }`}
          onClick={() =>
            goToSection("analytics")
          }
        >
          <span>◌</span>
          Analytics
        </button>

        <div className="sideStatus">
          <div className="onlineRow">
            <span className="onlineDot"></span>
            API Online
          </div>

          <p>
            U-Net inference engine active
          </p>
        </div>
      </aside>

      {/* =================================================
          MAIN
      ================================================= */}

      <main className="main">

        {/* =================================================
            TOP HEADER
        ================================================= */}

        <header className="topbar">

          <div>
            <h2>
              Landslide Risk Dashboard
            </h2>

            <p>
              AI-powered monitoring and early
              warning intelligence
            </p>
          </div>

          <div className="topActions">

            <div className="liveBadge">
              <span></span>
              System Live
            </div>

            <button
              className="refreshButton"
              onClick={() => {
                if (
                  currentPrediction
                ) {
                  setData(
                    buildDashboardFromPrediction(
                      {
                        prediction:
                          currentPrediction,
                      }
                    )
                  );
                } else {
                  loadDashboard();
                }
              }}
            >
              ↻ Refresh
            </button>
          </div>
        </header>

        {/* =================================================
            DASHBOARD
        ================================================= */}

        <section id="dashboard">

          {/* HERO */}

          <section className="hero">

            <div className="heroGlow"></div>

            <div className="heroContent">

              <div className="eyebrow">
                AI-BASED EARLY WARNING SYSTEM
              </div>

              <h3>
                Intelligent Landslide Risk
                Monitoring
              </h3>

              <p>
                LandslideAI analyzes multi-channel
                geospatial imagery using a
                deep-learning segmentation model
                to identify potential landslide
                regions and generate preliminary
                risk indicators for monitoring and
                early-warning workflows.
              </p>

              <div className="chips">

                <span>
                  🧠 U-Net
                </span>

                <span>
                  🛰️ 14 Channels
                </span>

                <span>
                  📊 {total} Predictions
                </span>

                <span>
                  ⚡ Risk Engine Active
                </span>
              </div>
            </div>
          </section>

          {error && (
            <div className="errorBox">
              ⚠️ {error}
            </div>
          )}

          {/* KPI */}

          <section className="kpiGrid">

            <div className="card kpiCard">
              <div className="kpiHeader">
                <span>
                  IMAGES ANALYZED
                </span>

                <div className="kpiIcon blue">
                  🛰️
                </div>
              </div>

              <strong>
                {loading
                  ? "..."
                  : total}
              </strong>

              <p>
                Prediction records available
              </p>
            </div>

            <div className="card kpiCard">
              <div className="kpiHeader">
                <span>
                  AVERAGE RISK
                </span>

                <div className="kpiIcon cyan">
                  📈
                </div>
              </div>

              <strong>
                {loading
                  ? "..."
                  : averageRisk.toFixed(
                      2
                    )}
              </strong>

              <p>
                Preliminary AI-derived score
              </p>
            </div>

            <div className="card kpiCard">
              <div className="kpiHeader">
                <span>
                  HIGH RISK
                </span>

                <div className="kpiIcon orange">
                  ⚠️
                </div>
              </div>

              <strong>
                {loading
                  ? "..."
                  : highRisk}
              </strong>

              <p>
                High + very high predictions
              </p>
            </div>

            <div className="card kpiCard">
              <div className="kpiHeader">
                <span>
                  MAXIMUM RISK
                </span>

                <div className="kpiIcon red">
                  🚨
                </div>
              </div>

              <strong>
                {loading
                  ? "..."
                  : maximumRisk.toFixed(
                      2
                    )}
              </strong>

              <p>
                Highest detected risk score
              </p>
            </div>
          </section>

          {/* =================================================
              UPLOAD
          ================================================= */}

          <section
            className="card panel"
            style={{
              marginTop: "20px",
            }}
          >
            <div className="panelHeader">

              <div>
                <h3>
                  Upload Satellite Image
                </h3>

                <p>
                  Upload a 128 × 128 ×
                  14-channel H5 image to
                  generate a new AI landslide
                  risk prediction.
                </p>
              </div>

              <span className="smallBadge">
                AI Prediction
              </span>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "minmax(0, 1fr) auto",
                gap: "16px",
                alignItems: "center",
                marginTop: "18px",
              }}
            >

              <div>

                <label
                  htmlFor="h5-upload"
                  style={{
                    display: "block",
                    marginBottom: "8px",
                    fontWeight: "700",
                    color: "#dce6f5",
                  }}
                >
                  Select H5 satellite image
                </label>

                <input
                  id="h5-upload"
                  type="file"
                  accept=".h5"
                  onChange={
                    handleFileChange
                  }
                  style={{
                    width: "100%",
                    padding: "12px",
                    borderRadius: "10px",
                    border:
                      "1px solid rgba(148,163,184,0.25)",
                    background:
                      "rgba(15,23,42,0.8)",
                    color: "#dce6f5",
                  }}
                />

                {selectedFile && (
                  <div
                    style={{
                      marginTop: "8px",
                      fontSize: "13px",
                      color: "#8fa3bd",
                    }}
                  >
                    Selected:{" "}
                    <strong>
                      {selectedFile.name}
                    </strong>
                  </div>
                )}
              </div>

              <button
                className="refreshButton"
                onClick={
                  handlePredictUpload
                }
                disabled={uploading}
                style={{
                  minWidth: "170px",
                  height: "48px",
                  cursor: uploading
                    ? "not-allowed"
                    : "pointer",
                  opacity: uploading
                    ? 0.7
                    : 1,
                }}
              >
                {uploading
                  ? "⏳ Predicting..."
                  : "🚀 Predict Risk"}
              </button>
            </div>

            {uploadError && (
              <div
                className="errorBox"
                style={{
                  marginTop: "16px",
                }}
              >
                ⚠️ {uploadError}
              </div>
            )}

            {/* RESULT */}

            {uploadResult && (
              <div
                style={{
                  marginTop: "24px",
                  padding: "20px",
                  borderRadius: "16px",
                  border:
                    "1px solid rgba(59,130,246,0.25)",
                  background:
                    "rgba(15,23,42,0.65)",
                }}
              >

                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                    alignItems: "center",
                    gap: "16px",
                    flexWrap: "wrap",
                    marginBottom: "18px",
                  }}
                >

                  <div>

                    <div
                      style={{
                        color: "#8fa3bd",
                        fontSize: "12px",
                        marginBottom: "4px",
                      }}
                    >
                      PREDICTION RESULT
                    </div>

                    <h3
                      style={{
                        margin: 0,
                      }}
                    >
                      {
                        uploadResult.filename
                      }
                    </h3>
                  </div>

                  <span
                    style={{
                      padding:
                        "8px 14px",
                      borderRadius:
                        "999px",
                      background:
                        "rgba(59,130,246,0.14)",
                      border:
                        "1px solid rgba(59,130,246,0.25)",
                      color: "#93c5fd",
                      fontWeight:
                        "800",
                    }}
                  >
                    {
                      userPrediction?.risk_level
                    }
                  </span>
                </div>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "repeat(4, minmax(0, 1fr))",
                    gap: "12px",
                  }}
                >

                  <div className="card">
                    <span>
                      Predicted Area
                    </span>

                    <strong
                      style={{
                        display: "block",
                        marginTop:
                          "8px",
                        fontSize:
                          "24px",
                      }}
                    >
                      {userPrediction
                        ?.predicted_area_percent
                        ?.toFixed(
                          2
                        ) ?? "0.00"}
                      %
                    </strong>
                  </div>

                  <div className="card">
                    <span>
                      Mean Probability
                    </span>

                    <strong
                      style={{
                        display: "block",
                        marginTop:
                          "8px",
                        fontSize:
                          "24px",
                      }}
                    >
                      {(
                        (
                          userPrediction?.mean_probability ??
                          0
                        ) * 100
                      ).toFixed(
                        2
                      )}
                      %
                    </strong>
                  </div>

                  <div className="card">
                    <span>
                      Max Probability
                    </span>

                    <strong
                      style={{
                        display: "block",
                        marginTop:
                          "8px",
                        fontSize:
                          "24px",
                      }}
                    >
                      {(
                        (
                          userPrediction?.max_probability ??
                          0
                        ) * 100
                      ).toFixed(
                        2
                      )}
                      %
                    </strong>
                  </div>

                  <div className="card">
                    <span>
                      Risk Score
                    </span>

                    <strong
                      style={{
                        display: "block",
                        marginTop:
                          "8px",
                        fontSize:
                          "24px",
                      }}
                    >
                      {userPrediction
                        ?.risk_score
                        ?.toFixed(
                          2
                        ) ?? "0.00"}
                      /100
                    </strong>
                  </div>
                </div>

                <div
                  style={{
                    marginTop: "16px",
                    color: "#8fa3bd",
                    fontSize: "13px",
                  }}
                >
                  Input shape:{" "}
                  {uploadResult.input_shape?.join(
                    " × "
                  )}
                  {" | "}
                  Prediction generated by U-Net
                </div>
              </div>
            )}
          </section>

          {/* =================================================
              HIGH-RISK MONITORING
          ================================================= */}

          <section className="lowerGrid">

            <div className="card panel">

              <div className="panelHeader">

                <div>
                  <h3>
                    High-Risk Monitoring
                  </h3>

                  <p>
                    Current priority indicators
                  </p>
                </div>
              </div>

              <div className="alertCard danger">

                <div className="alertIcon">
                  🚨
                </div>

                <div>

                  <strong>
                    Very High Risk Zones
                    Detected
                  </strong>

                  <p>
                    {data?.very_high ?? 0}{" "}
                    prediction tile is
                    currently classified as
                    very high preliminary risk.
                  </p>
                </div>
              </div>

              <div className="alertCard warning">

                <div className="alertIcon">
                  ⚠️
                </div>

                <div>

                  <strong>
                    High-Risk Areas Require
                    Review
                  </strong>

                  <p>
                    {data?.high ?? 0}{" "}
                    prediction tile has
                    generated high-risk
                    indicators.
                  </p>
                </div>
              </div>
            </div>

            <div className="card panel">

              <div className="panelHeader">

                <div>
                  <h3>
                    AI Monitoring Note
                  </h3>

                  <p>
                    Interpretation guidance
                  </p>
                </div>
              </div>

              <div className="infoBox">

                <div className="infoIcon">
                  🧠
                </div>

                <p>
                  The current risk score is a
                  preliminary AI-derived indicator
                  based on model predictions. It
                  should be used for monitoring and
                  prioritization, not as an official
                  government hazard classification.
                </p>
              </div>
            </div>
          </section>
        </section>

        {/* =================================================
            ANALYTICS
        ================================================= */}

        <section id="analytics">
          <AnalyticsCards
            data={data}
          />
        </section>

        {/* =================================================
            AI PREDICTIONS
        ================================================= */}

        <section id="ai-predictions">
          <Predictions
            currentPrediction={
              currentPrediction
            }
          />
        </section>

        {/* =================================================
            RISK ALERTS
        ================================================= */}

        <section id="risk-alerts">
          <RiskAlerts
            currentPrediction={
              currentPrediction
            }
          />
        </section>

        {/* =================================================
            PRECAUTIONS — LAST SECTION
        ================================================= */}

        {uploadResult &&
          userPrediction && (
            <section
              id="precautions"
              className="card panel"
              style={{
                marginTop: "20px",
              }}
            >
              <div className="panelHeader">

                <div>
                  <h3>
                    🛡️ Recommended Precautions
                  </h3>

                  <p>
                    Risk-level based monitoring
                    guidance for the current prediction
                  </p>
                </div>

                <span className="smallBadge">
                  {
                    userPrediction.risk_level
                  }
                </span>
              </div>

              <div
                style={{
                  marginTop: "16px",
                  display: "grid",
                  gap: "12px",
                }}
              >
                {getPrecautions(
                  userPrediction.risk_level
                ).map(
                  (
                    precaution,
                    index
                  ) => (
                    <div
                      key={index}
                      style={{
                        display: "flex",
                        alignItems:
                          "flex-start",
                        gap: "12px",
                        padding:
                          "14px 16px",
                        borderRadius:
                          "12px",
                        background:
                          "rgba(15,23,42,0.55)",
                        border:
                          "1px solid rgba(148,163,184,0.16)",
                      }}
                    >
                      <span
                        style={{
                          fontSize:
                            "18px",
                          lineHeight:
                            "1",
                        }}
                      >
                        🛡️
                      </span>

                      <span
                        style={{
                          color:
                            "#dce6f5",
                          fontSize:
                            "14px",
                          lineHeight:
                            "1.5",
                        }}
                      >
                        {
                          precaution
                        }
                      </span>
                    </div>
                  )
                )}
              </div>

              <div
                style={{
                  marginTop: "16px",
                  padding:
                    "12px 14px",
                  borderRadius:
                    "10px",
                  background:
                    "rgba(59,130,246,0.08)",
                  color:
                    "#8fa3bd",
                  fontSize:
                    "12px",
                  lineHeight:
                    "1.5",
                }}
              >
                🧠 These are preliminary
                AI-based monitoring
                recommendations. They do not
                replace official hazard warnings,
                professional assessment, or
                instructions from local authorities.
              </div>
            </section>
          )}

        {/* =================================================
            FOOTER
        ================================================= */}

        <footer>
          LandslideAI · AI-Based Early Warning
          and Landslide Risk Monitoring System
        </footer>

      </main>
    </div>
  );
}

export default App;