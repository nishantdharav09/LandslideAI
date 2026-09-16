import {
  useEffect,
  useMemo,
  useState,
} from "react";

const API_BASE =
  "http://127.0.0.1:8010";

function Predictions({
  currentPrediction,
}) {
  const [predictions, setPredictions] =
    useState([]);

  const [selectedImage, setSelectedImage] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [search, setSearch] =
    useState("");

  const [riskFilter, setRiskFilter] =
    useState("All");

  const [sortOrder, setSortOrder] =
    useState("high");

  /* =====================================================
     OLD PREDICTIONS
  ===================================================== */

  const loadPredictions =
    async () => {
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
              "Prediction API error"
          );
        }

        const records =
          result.data || [];

        setPredictions(
          records
        );

        if (
          records.length > 0
        ) {
          setSelectedImage(
            records[0]
          );
        }
      } catch (err) {
        console.error(
          "Predictions API error:",
          err
        );

        setError(
          "Unable to load AI predictions."
        );
      } finally {
        setLoading(false);
      }
    };

  /* =====================================================
     INITIAL LOAD
  ===================================================== */

  useEffect(() => {
    if (!currentPrediction) {
      loadPredictions();
    }
  }, [currentPrediction]);

  /* =====================================================
     CURRENT UPLOAD
  ===================================================== */

  useEffect(() => {
    if (currentPrediction) {
      setPredictions([
        currentPrediction,
      ]);

      setSelectedImage(
        currentPrediction
      );

      setLoading(false);
      setError("");
    }
  }, [currentPrediction]);

  /* =====================================================
     RISK CLASS
  ===================================================== */

  const getRiskClass =
    (level) => {
      if (
        level === "Very High"
      ) {
        return "riskVeryHigh";
      }

      if (level === "High") {
        return "riskHigh";
      }

      if (
        level === "Moderate"
      ) {
        return "riskModerate";
      }

      return "riskLow";
    };

  /* =====================================================
     FILTER + SORT
  ===================================================== */

  const filteredPredictions =
    useMemo(() => {
      let result = [
        ...predictions,
      ];

      if (search.trim()) {
        const query =
          search.toLowerCase();

        result =
          result.filter(
            (item) =>
              item.image
                .toLowerCase()
                .includes(query)
          );
      }

      if (
        riskFilter !== "All"
      ) {
        result =
          result.filter(
            (item) =>
              item.risk_level ===
              riskFilter
          );
      }

      result.sort(
        (a, b) => {
          if (
            sortOrder === "high"
          ) {
            return (
              b.risk_score -
              a.risk_score
            );
          }

          if (
            sortOrder === "low"
          ) {
            return (
              a.risk_score -
              b.risk_score
            );
          }

          if (
            sortOrder === "area"
          ) {
            return (
              b.predicted_area_percent -
              a.predicted_area_percent
            );
          }

          return 0;
        }
      );

      return result;
    }, [
      predictions,
      search,
      riskFilter,
      sortOrder,
    ]);

  /* =====================================================
     VISUALIZATION
  ===================================================== */

  const getVisualizationUrl =
    (item) => {
      if (
        item?.prediction_id
      ) {
        return (
          `${API_BASE}/api/upload-prediction/` +
          `${item.prediction_id}/visualization`
        );
      }

      return (
        `${API_BASE}/api/prediction/` +
        `${item.image}/visualization`
      );
    };

  return (
    <section className="predictionPanel">

      <div className="predictionHeader">

        <div>
          <h2>
            AI Predictions
          </h2>

          <p>
            {currentPrediction
              ? "Prediction generated from the latest uploaded satellite image"
              : "Highest-risk prediction tiles generated by LandslideAI"}
          </p>
        </div>

        <button
          className="refreshButton"
          onClick={() => {
            if (
              currentPrediction
            ) {
              setPredictions([
                currentPrediction,
              ]);

              setSelectedImage(
                currentPrediction
              );
            } else {
              loadPredictions();
            }
          }}
        >
          ↻ Refresh
        </button>
      </div>

      <div className="predictionFilters">

        <div className="searchBox">

          <span>🔎</span>

          <input
            type="text"
            placeholder="Search image..."
            value={search}
            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
          />
        </div>

        <select
          value={riskFilter}
          onChange={(e) =>
            setRiskFilter(
              e.target.value
            )
          }
        >
          <option value="All">
            All Risk Levels
          </option>

          <option value="Very High">
            Very High
          </option>

          <option value="High">
            High
          </option>

          <option value="Moderate">
            Moderate
          </option>

          <option value="Low">
            Low
          </option>
        </select>

        <select
          value={sortOrder}
          onChange={(e) =>
            setSortOrder(
              e.target.value
            )
          }
        >
          <option value="high">
            Highest Risk
          </option>

          <option value="low">
            Lowest Risk
          </option>

          <option value="area">
            Largest Area
          </option>
        </select>
      </div>

      {!loading &&
        !error && (
          <div className="predictionResultInfo">
            Showing{" "}
            <strong>
              {
                filteredPredictions.length
              }
            </strong>{" "}
            of{" "}
            <strong>
              {predictions.length}
            </strong>{" "}
            loaded predictions
          </div>
        )}

      {loading && (
        <div className="predictionLoading">
          Loading AI predictions...
        </div>
      )}

      {error && (
        <div className="predictionError">
          ⚠️ {error}
        </div>
      )}

      {!loading &&
        !error && (
          <>
            {filteredPredictions.length ===
            0 ? (
              <div className="predictionLoading">
                🔎 No predictions match
                your filter.
              </div>
            ) : (
              <div className="predictionTableWrapper">

                <table className="predictionTable">

                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Image</th>
                      <th>
                        Predicted Area
                      </th>
                      <th>
                        Mean Probability
                      </th>
                      <th>
                        Max Probability
                      </th>
                      <th>
                        Risk Score
                      </th>
                      <th>
                        Risk Level
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {filteredPredictions.map(
                      (
                        item,
                        index
                      ) => (
                        <tr
                          key={
                            item.image
                          }
                          onClick={() =>
                            setSelectedImage(
                              item
                            )
                          }
                          className={
                            selectedImage?.image ===
                            item.image
                              ? "selectedPrediction"
                              : ""
                          }
                        >
                          <td>
                            {index + 1}
                          </td>

                          <td className="imageName">
                            {item.image}
                          </td>

                          <td>
                            {item
                              .predicted_area_percent
                              .toFixed(
                                2
                              )}
                            %
                          </td>

                          <td>
                            {(
                              item
                                .mean_probability *
                              100
                            ).toFixed(
                              2
                            )}
                            %
                          </td>

                          <td>
                            {(
                              item
                                .max_probability *
                              100
                            ).toFixed(
                              2
                            )}
                            %
                          </td>

                          <td className="riskScore">
                            {item.risk_score.toFixed(
                              2
                            )}
                          </td>

                          <td>
                            <span
                              className={`riskBadge ${getRiskClass(
                                item.risk_level
                              )}`}
                            >
                              {
                                item.risk_level
                              }
                            </span>
                          </td>
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {selectedImage && (
              <div className="predictionViewer">

                <div className="viewerHeader">

                  <div>

                    <h3>
                      Prediction Explorer
                    </h3>

                    <p>
                      Selected:{" "}
                      {
                        selectedImage.image
                      }
                    </p>
                  </div>

                  <span
                    className={`riskBadge ${getRiskClass(
                      selectedImage.risk_level
                    )}`}
                  >
                    {
                      selectedImage.risk_level
                    }
                  </span>
                </div>

                <div className="visualizationContainer">

                  <img
                    src={getVisualizationUrl(
                      selectedImage
                    )}
                    alt={`${selectedImage.image} visualization`}
                  />
                </div>

                <div className="predictionMetrics">

                  <div>
                    <span>
                      Predicted Area
                    </span>

                    <strong>
                      {selectedImage
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
                        selectedImage
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
                        selectedImage
                          .max_probability *
                        100
                      ).toFixed(
                        2
                      )}
                      %
                    </strong>
                  </div>

                  <div>
                    <span>
                      Risk Score
                    </span>

                    <strong>
                      {selectedImage.risk_score.toFixed(
                        2
                      )}
                    </strong>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
    </section>
  );
}

export default Predictions;