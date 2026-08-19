/* Generated from data/final/combined_100_samples.csv. Do not include ground-truth labels here. */
window.APP_CONFIG = {
  "studyId": "cxr_gradcam_reader_study",
  "studyTitle": "CXR Heatmap Reader Study",
  "studySubtitle": "Initial diagnosis vs. Grad-CAM-assisted diagnosis",
  "randomizeCaseOrder": true,
  "randomizeHeatmapOrder": true,
  "blindModelNames": true,
  "askHelpfulHeatmaps": true,
  "diagnosisExclusiveLabels": [
    "No finding"
  ],
  "confidenceLevels": [
    {
      "value": "1",
      "label": "1 - Very unsure"
    },
    {
      "value": "2",
      "label": "2 - Somewhat unsure"
    },
    {
      "value": "3",
      "label": "3 - Moderately confident"
    },
    {
      "value": "4",
      "label": "4 - Confident"
    },
    {
      "value": "5",
      "label": "5 - Very confident"
    }
  ],
  "labels": [
    "None of these findings",
    "Tuberculosis",
    "Atelectasis",
    "Calcification",
    "Consolidation",
    "Fibrosis",
    "Nodule",
    "Pleural effusion",
    "Pneumonia",
    "Pneumothorax",
    "Thickened pleura",
    "Lung opacity",
    "Lung cavity",
    "Pulmonary edema"
  ],
  "cases": [
    {
      "case_id": "vindr_sample_0000",
      "cxr": "assets/cxr/vindr/sample_0000_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0000_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0000_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0000_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0001",
      "cxr": "assets/cxr/vindr/sample_0001_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0001_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0001_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0001_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0002",
      "cxr": "assets/cxr/vindr/sample_0002_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0002_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0002_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0002_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0003",
      "cxr": "assets/cxr/vindr/sample_0003_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0003_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0003_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0003_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0004",
      "cxr": "assets/cxr/vindr/sample_0004_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0004_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0004_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0004_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0005",
      "cxr": "assets/cxr/vindr/sample_0005_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0005_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0005_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0005_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0006",
      "cxr": "assets/cxr/vindr/sample_0006_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0006_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0006_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0006_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0007",
      "cxr": "assets/cxr/vindr/sample_0007_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0007_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0007_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0007_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0008",
      "cxr": "assets/cxr/vindr/sample_0008_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0008_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0008_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0008_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0009",
      "cxr": "assets/cxr/vindr/sample_0009_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0009_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0009_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0009_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0010",
      "cxr": "assets/cxr/vindr/sample_0010_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0010_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0010_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0010_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0011",
      "cxr": "assets/cxr/vindr/sample_0011_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0011_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0011_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0011_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0012",
      "cxr": "assets/cxr/vindr/sample_0012_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0012_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0012_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0012_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0013",
      "cxr": "assets/cxr/vindr/sample_0013_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0013_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0013_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0013_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0014",
      "cxr": "assets/cxr/vindr/sample_0014_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0014_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0014_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0014_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0015",
      "cxr": "assets/cxr/vindr/sample_0015_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0015_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0015_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0015_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0016",
      "cxr": "assets/cxr/vindr/sample_0016_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0016_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0016_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0016_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0017",
      "cxr": "assets/cxr/vindr/sample_0017_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0017_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0017_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0017_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0018",
      "cxr": "assets/cxr/vindr/sample_0018_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0018_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0018_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0018_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0019",
      "cxr": "assets/cxr/vindr/sample_0019_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0019_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0019_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0019_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0020",
      "cxr": "assets/cxr/vindr/sample_0020_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0020_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0020_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0020_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0021",
      "cxr": "assets/cxr/vindr/sample_0021_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0021_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0021_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0021_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0022",
      "cxr": "assets/cxr/vindr/sample_0022_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0022_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0022_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0022_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0023",
      "cxr": "assets/cxr/vindr/sample_0023_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0023_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0023_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0023_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0024",
      "cxr": "assets/cxr/vindr/sample_0024_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0024_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0024_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0024_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0025",
      "cxr": "assets/cxr/vindr/sample_0025_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0025_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0025_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0025_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0026",
      "cxr": "assets/cxr/vindr/sample_0026_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0026_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0026_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0026_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0027",
      "cxr": "assets/cxr/vindr/sample_0027_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0027_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0027_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0027_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0028",
      "cxr": "assets/cxr/vindr/sample_0028_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0028_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0028_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0028_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0029",
      "cxr": "assets/cxr/vindr/sample_0029_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0029_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0029_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0029_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0030",
      "cxr": "assets/cxr/vindr/sample_0030_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0030_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0030_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0030_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0031",
      "cxr": "assets/cxr/vindr/sample_0031_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0031_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0031_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0031_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0032",
      "cxr": "assets/cxr/vindr/sample_0032_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0032_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0032_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0032_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0033",
      "cxr": "assets/cxr/vindr/sample_0033_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0033_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0033_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0033_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0034",
      "cxr": "assets/cxr/vindr/sample_0034_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0034_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0034_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0034_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0035",
      "cxr": "assets/cxr/vindr/sample_0035_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0035_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0035_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0035_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0036",
      "cxr": "assets/cxr/vindr/sample_0036_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0036_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0036_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0036_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0037",
      "cxr": "assets/cxr/vindr/sample_0037_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0037_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0037_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0037_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0038",
      "cxr": "assets/cxr/vindr/sample_0038_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0038_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0038_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0038_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0039",
      "cxr": "assets/cxr/vindr/sample_0039_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0039_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0039_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0039_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0040",
      "cxr": "assets/cxr/vindr/sample_0040_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0040_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0040_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0040_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0041",
      "cxr": "assets/cxr/vindr/sample_0041_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0041_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0041_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0041_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0042",
      "cxr": "assets/cxr/vindr/sample_0042_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0042_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0042_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0042_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0043",
      "cxr": "assets/cxr/vindr/sample_0043_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0043_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0043_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0043_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0044",
      "cxr": "assets/cxr/vindr/sample_0044_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0044_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0044_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0044_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0045",
      "cxr": "assets/cxr/vindr/sample_0045_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0045_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0045_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0045_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0046",
      "cxr": "assets/cxr/vindr/sample_0046_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0046_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0046_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0046_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0047",
      "cxr": "assets/cxr/vindr/sample_0047_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0047_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0047_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0047_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0048",
      "cxr": "assets/cxr/vindr/sample_0048_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0048_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0048_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0048_cam.png"
        }
      ]
    },
    {
      "case_id": "vindr_sample_0049",
      "cxr": "assets/cxr/vindr/sample_0049_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/vindr/sample_0049_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/vindr/sample_0049_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/vindr/sample_0049_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0000",
      "cxr": "assets/cxr/chestdr/sample_0000_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0000_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0000_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0000_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0001",
      "cxr": "assets/cxr/chestdr/sample_0001_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0001_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0001_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0001_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0002",
      "cxr": "assets/cxr/chestdr/sample_0002_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0002_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0002_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0002_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0003",
      "cxr": "assets/cxr/chestdr/sample_0003_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0003_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0003_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0003_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0004",
      "cxr": "assets/cxr/chestdr/sample_0004_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0004_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0004_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0004_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0005",
      "cxr": "assets/cxr/chestdr/sample_0005_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0005_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0005_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0005_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0006",
      "cxr": "assets/cxr/chestdr/sample_0006_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0006_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0006_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0006_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0007",
      "cxr": "assets/cxr/chestdr/sample_0007_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0007_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0007_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0007_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0008",
      "cxr": "assets/cxr/chestdr/sample_0008_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0008_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0008_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0008_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0009",
      "cxr": "assets/cxr/chestdr/sample_0009_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0009_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0009_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0009_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0010",
      "cxr": "assets/cxr/chestdr/sample_0010_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0010_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0010_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0010_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0011",
      "cxr": "assets/cxr/chestdr/sample_0011_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0011_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0011_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0011_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0012",
      "cxr": "assets/cxr/chestdr/sample_0012_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0012_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0012_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0012_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0013",
      "cxr": "assets/cxr/chestdr/sample_0013_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0013_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0013_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0013_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0014",
      "cxr": "assets/cxr/chestdr/sample_0014_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0014_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0014_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0014_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0015",
      "cxr": "assets/cxr/chestdr/sample_0015_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0015_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0015_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0015_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0016",
      "cxr": "assets/cxr/chestdr/sample_0016_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0016_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0016_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0016_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0017",
      "cxr": "assets/cxr/chestdr/sample_0017_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0017_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0017_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0017_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0018",
      "cxr": "assets/cxr/chestdr/sample_0018_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0018_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0018_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0018_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0019",
      "cxr": "assets/cxr/chestdr/sample_0019_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0019_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0019_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0019_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0020",
      "cxr": "assets/cxr/chestdr/sample_0020_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0020_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0020_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0020_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0021",
      "cxr": "assets/cxr/chestdr/sample_0021_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0021_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0021_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0021_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0022",
      "cxr": "assets/cxr/chestdr/sample_0022_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0022_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0022_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0022_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0023",
      "cxr": "assets/cxr/chestdr/sample_0023_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0023_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0023_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0023_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0024",
      "cxr": "assets/cxr/chestdr/sample_0024_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0024_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0024_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0024_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0025",
      "cxr": "assets/cxr/chestdr/sample_0025_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0025_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0025_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0025_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0026",
      "cxr": "assets/cxr/chestdr/sample_0026_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0026_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0026_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0026_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0027",
      "cxr": "assets/cxr/chestdr/sample_0027_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0027_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0027_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0027_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0028",
      "cxr": "assets/cxr/chestdr/sample_0028_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0028_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0028_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0028_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0029",
      "cxr": "assets/cxr/chestdr/sample_0029_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0029_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0029_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0029_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0030",
      "cxr": "assets/cxr/chestdr/sample_0030_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0030_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0030_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0030_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0031",
      "cxr": "assets/cxr/chestdr/sample_0031_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0031_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0031_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0031_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0032",
      "cxr": "assets/cxr/chestdr/sample_0032_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0032_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0032_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0032_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0033",
      "cxr": "assets/cxr/chestdr/sample_0033_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0033_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0033_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0033_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0034",
      "cxr": "assets/cxr/chestdr/sample_0034_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0034_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0034_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0034_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0035",
      "cxr": "assets/cxr/chestdr/sample_0035_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0035_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0035_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0035_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0036",
      "cxr": "assets/cxr/chestdr/sample_0036_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0036_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0036_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0036_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0037",
      "cxr": "assets/cxr/chestdr/sample_0037_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0037_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0037_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0037_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0038",
      "cxr": "assets/cxr/chestdr/sample_0038_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0038_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0038_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0038_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0039",
      "cxr": "assets/cxr/chestdr/sample_0039_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0039_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0039_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0039_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0040",
      "cxr": "assets/cxr/chestdr/sample_0040_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0040_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0040_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0040_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0041",
      "cxr": "assets/cxr/chestdr/sample_0041_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0041_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0041_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0041_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0042",
      "cxr": "assets/cxr/chestdr/sample_0042_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0042_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0042_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0042_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0043",
      "cxr": "assets/cxr/chestdr/sample_0043_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0043_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0043_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0043_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0044",
      "cxr": "assets/cxr/chestdr/sample_0044_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0044_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0044_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0044_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0045",
      "cxr": "assets/cxr/chestdr/sample_0045_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0045_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0045_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0045_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0046",
      "cxr": "assets/cxr/chestdr/sample_0046_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0046_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0046_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0046_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0047",
      "cxr": "assets/cxr/chestdr/sample_0047_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0047_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0047_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0047_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0048",
      "cxr": "assets/cxr/chestdr/sample_0048_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0048_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0048_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0048_cam.png"
        }
      ]
    },
    {
      "case_id": "chestdr_sample_0049",
      "cxr": "assets/cxr/chestdr/sample_0049_input.png",
      "heatmaps": [
        {
          "model_id": "ark",
          "display_name": "ARK",
          "src": "assets/heatmaps/ark/chestdr/sample_0049_cam.png"
        },
        {
          "model_id": "eva",
          "display_name": "EVA",
          "src": "assets/heatmaps/eva/chestdr/sample_0049_cam.png"
        },
        {
          "model_id": "raddino",
          "display_name": "RADDINO",
          "src": "assets/heatmaps/raddino/chestdr/sample_0049_cam.png"
        }
      ]
    }
  ]
};
