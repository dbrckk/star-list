This file is a merged representation of a subset of the codebase, containing specifically included files and files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/*.{py,js,mjs,cjs,ts,tsx,jsx,java,kt,kts,gd,groovy,gradle,toml,json,yaml,yml,sql,sh}
- Files matching these patterns are excluded: .ai/**, **/node_modules/**, **/.gradle/**, **/build/**, **/dist/**, **/.venv/**, **/__pycache__/**, **/.pytest_cache/**, **/.git/**, **/coverage/**, **/*.lock, **/*.min.js, **/*.map, assets/**, art/**, art_sources/**, marketing/**, colab/**, kaggle/**, discovery-cache.json, health-snapshot.json, history.json
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
agent-skill-source-audit.schema.json
cache-health-history.schema.json
cache-health-trend.schema.json
cache-health.schema.json
catalog-quality.schema.json
catalog-stats.schema.json
coverage-report.schema.json
discovery-cache.schema.json
discovery-candidates.schema.json
discovery-evaluated.schema.json
discovery-memory.schema.json
discovery-watchlist.schema.json
github-id-backfill-report.schema.json
health-drift.schema.json
health-snapshot.schema.json
health-trends.schema.json
history.schema.json
metadata-evidence.schema.json
readme-domain-evidence.schema.json
replacement-report.schema.json
star-sync-report.schema.json
websites.schema.json
```

# Files

## File: agent-skill-source-audit.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Pinned Skill Source Metadata Audit",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "checkedAt",
    "mode",
    "total",
    "coverageComplete",
    "counts",
    "findings",
    "sourceContentReviewed",
    "automaticInstallation",
    "entries"
  ],
  "properties": {
    "schemaVersion": {
      "const": 1
    },
    "checkedAt": {
      "type": "string",
      "minLength": 1
    },
    "mode": {
      "enum": [
        "online",
        "offline"
      ]
    },
    "total": {
      "type": "integer",
      "minimum": 1
    },
    "coverageComplete": {
      "type": "boolean"
    },
    "counts": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "verified",
        "missing",
        "invalid",
        "unavailable",
        "unchecked"
      ],
      "properties": {
        "verified": {
          "type": "integer",
          "minimum": 0
        },
        "missing": {
          "type": "integer",
          "minimum": 0
        },
        "invalid": {
          "type": "integer",
          "minimum": 0
        },
        "unavailable": {
          "type": "integer",
          "minimum": 0
        },
        "unchecked": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "findings": {
      "type": "integer",
      "minimum": 0
    },
    "sourceContentReviewed": {
      "const": false
    },
    "automaticInstallation": {
      "const": false
    },
    "entries": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "id",
          "sourceRepository",
          "sourceCommit",
          "sourcePath",
          "sourceUrl",
          "status",
          "reason"
        ],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"
          },
          "sourceRepository": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
          },
          "sourceCommit": {
            "type": "string",
            "pattern": "^[a-f0-9]{40}$"
          },
          "sourcePath": {
            "type": "string",
            "pattern": "^(?:[A-Za-z0-9_.-]+/)*SKILL[.]md$"
          },
          "sourceUrl": {
            "type": "string",
            "pattern": "^https://github[.]com/"
          },
          "status": {
            "enum": [
              "verified",
              "missing",
              "invalid",
              "unavailable",
              "unchecked"
            ]
          },
          "reason": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    }
  }
}
```

## File: cache-health-history.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health History","type":"object","required":["schemaVersion","points"],"properties":{"schemaVersion":{"type":"integer","const":1},"points":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health History Point","type":"object","required":["date","status","logicalRequests","apiCallAvoidanceRate","bodyReuseRate","networkFetchRate","staleFallbackRate"],"properties":{"date":{"type":"string","pattern":"^\\d{4}-\\d{2}-\\d{2}$"},"status":{"enum":["healthy","watch","degraded","unknown"]},"logicalRequests":{"type":"integer","minimum":0},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1},"networkFetchRate":{"type":"number","minimum":0,"maximum":1},"staleFallbackRate":{"type":"number","minimum":0,"maximum":1},"candidateSeverity":{"enum":["healthy","watch","degraded"]},"alertState":{"enum":["healthy","watch","degraded"]},"issueAction":{"enum":["open","hold","close"]}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: cache-health-trend.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health Trend","type":"object","required":["direction","findings","windowPoints","apiCallAvoidanceDelta","networkFetchDelta","adaptiveBaseline","adaptiveSeverity","candidateSeverity","alertState","issueAction"],"properties":{"direction":{"enum":["insufficient-data","declining","stable","improving"]},"findings":{"type":"array","items":{"type":"string"}},"windowPoints":{"type":"integer","minimum":0},"apiCallAvoidanceDelta":{"type":["number","null"]},"networkFetchDelta":{"type":["number","null"]},"bodyReuseDelta":{"type":["number","null"]},"fromDate":{"type":["string","null"]},"toDate":{"type":["string","null"]},"adaptiveBaseline":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Adaptive Cache Baseline","type":"object","required":["status","sampleSize","threshold","confidence","confidenceScore","findings"],"properties":{"status":{"enum":["insufficient-data","normal","anomalous"]},"sampleSize":{"type":"integer","minimum":0},"threshold":{"type":"number","minimum":0},"confidence":{"enum":["insufficient-data","low","medium","high"]},"confidenceScore":{"type":"number","minimum":0,"maximum":1},"findings":{"type":"array","items":{"type":"string"}},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1},"networkFetchRate":{"type":"number","minimum":0,"maximum":1},"deltas":{"type":"object","additionalProperties":{"type":"number"}}},"additionalProperties":true},"adaptiveSeverity":{"enum":["healthy","watch","degraded"]},"candidateSeverity":{"enum":["healthy","watch","degraded"]},"alertState":{"enum":["healthy","watch","degraded"]},"issueAction":{"enum":["open","hold","close"]}},"additionalProperties":false}
```

## File: cache-health.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health Report","type":"object","required":["status","findings","metrics"],"properties":{"status":{"enum":["healthy","watch","degraded"]},"findings":{"type":"array","items":{"type":"string"}},"metrics":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Cache Health Metrics","type":"object","required":["logicalRequests","freshCacheHits","notModifiedHits","staleFallbacks","networkFetches","apiCallAvoidanceRate","bodyReuseRate","networkFetchRate","staleFallbackRate"],"properties":{"logicalRequests":{"type":"integer","minimum":0},"freshCacheHits":{"type":"integer","minimum":0},"notModifiedHits":{"type":"integer","minimum":0},"staleFallbacks":{"type":"integer","minimum":0},"networkFetches":{"type":"integer","minimum":0},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1},"networkFetchRate":{"type":"number","minimum":0,"maximum":1},"staleFallbackRate":{"type":"number","minimum":0,"maximum":1}},"additionalProperties":false}},"additionalProperties":false}
```

## File: catalog-quality.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Catalog Quality Audit",
  "type": "object",
  "required": [
    "staleDays",
    "repositories",
    "summary",
    "guidanceCoverage",
    "identityCoverage",
    "findings"
  ],
  "properties": {
    "staleDays": {
      "type": "integer",
      "minimum": 1
    },
    "repositories": {
      "type": "integer",
      "minimum": 0
    },
    "summary": {
      "type": "object",
      "required": [
        "findings",
        "review",
        "info",
        "byCode"
      ],
      "properties": {
        "findings": {
          "type": "integer",
          "minimum": 0
        },
        "review": {
          "type": "integer",
          "minimum": 0
        },
        "info": {
          "type": "integer",
          "minimum": 0
        },
        "byCode": {
          "type": "object",
          "additionalProperties": {
            "type": "integer",
            "minimum": 0
          }
        }
      },
      "additionalProperties": false
    },
    "guidanceCoverage": {
      "type": "object",
      "required": [
        "bestFor",
        "avoidWhen",
        "alternatives",
        "complements"
      ],
      "properties": {
        "bestFor": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        },
        "avoidWhen": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        },
        "alternatives": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        },
        "complements": {
          "type": "object",
          "required": [
            "populated",
            "missing"
          ],
          "properties": {
            "populated": {
              "type": "integer",
              "minimum": 0
            },
            "missing": {
              "type": "integer",
              "minimum": 0
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "identityCoverage": {
      "type": "object",
      "required": ["verified", "missing"],
      "properties": {
        "verified": {"type": "integer", "minimum": 0},
        "missing": {"type": "integer", "minimum": 0}
      },
      "additionalProperties": false
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repo",
          "severity",
          "code",
          "message"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "minLength": 1
          },
          "severity": {
            "enum": [
              "review",
              "info"
            ]
          },
          "code": {
            "type": "string",
            "minLength": 1
          },
          "message": {
            "type": "string",
            "minLength": 1
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

## File: catalog-stats.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Catalog Statistics","type":"object","required":["repositories","averageScore","selfHosted","selfHostedPercent","domains","tiers","topLanguages","topPlatforms","topCapabilities","domainLeaders"],"properties":{"repositories":{"type":"integer","minimum":0},"averageScore":{"type":"number"},"selfHosted":{"type":"integer","minimum":0},"selfHostedPercent":{"type":"number","minimum":0,"maximum":100},"domains":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"tiers":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"topLanguages":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"topPlatforms":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"topCapabilities":{"type":"object","additionalProperties":{"type":"integer","minimum":0}},"domainLeaders":{"type":"object","additionalProperties":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Domain Leader","type":"object","required":["repo","score","tier"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"score":{"type":["number","null"]},"tier":{"type":["string","null"]}},"additionalProperties":false}}}},"additionalProperties":false}
```

## File: coverage-report.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Coverage Report","type":"object","required":["policy","domainGaps","capabilityGaps","qualityGaps","summary"],"properties":{"policy":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Coverage Policy","type":"object","required":["minHealthyPerDomain","minHealthyPerCapability"],"properties":{"minHealthyPerDomain":{"type":"integer","minimum":1},"minHealthyPerCapability":{"type":"integer","minimum":1}},"additionalProperties":false},"domainGaps":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Domain Gap","type":"object","required":["domain","total","healthy","deficit","severity"],"properties":{"domain":{"type":"string","minLength":1},"total":{"type":"integer","minimum":0},"healthy":{"type":"integer","minimum":0},"deficit":{"type":"integer","minimum":0},"severity":{"enum":["critical","warning"]}},"additionalProperties":false}},"capabilityGaps":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Capability Gap","type":"object","required":["capability","total","healthy","deficit","severity"],"properties":{"capability":{"type":"string","minLength":1},"total":{"type":"integer","minimum":0},"healthy":{"type":"integer","minimum":0},"deficit":{"type":"integer","minimum":0},"severity":{"enum":["critical","warning"]}},"additionalProperties":false}},"qualityGaps":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Quality Gap","type":"object","required":["domain","repositories","issue"],"properties":{"domain":{"type":"string","minLength":1},"repositories":{"type":"integer","minimum":0},"issue":{"type":"string","minLength":1}},"additionalProperties":false}},"summary":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Coverage Summary","type":"object","required":["domains","capabilities","domainGaps","capabilityGaps","qualityGaps"],"properties":{"domains":{"type":"integer","minimum":0},"capabilities":{"type":"integer","minimum":0},"domainGaps":{"type":"integer","minimum":0},"capabilityGaps":{"type":"integer","minimum":0},"qualityGaps":{"type":"integer","minimum":0}},"additionalProperties":false}},"additionalProperties":false}
```

## File: discovery-cache.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Cache","type":"object","required":["schemaVersion","entries"],"properties":{"schemaVersion":{"type":"integer","const":1},"entries":{"type":"object","additionalProperties":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Cache Entry","type":"object","required":["fetchedAt","data","headers"],"properties":{"fetchedAt":{"type":"number","minimum":0},"data":{},"headers":{"type":"object"}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: discovery-candidates.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Candidates","type":"object","required":["candidates","repositories","errors","staleSources","cacheStats"],"properties":{"candidates":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"type":"object","required":["repo","stars","forks","discoveryScore","matchedTargets"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"url":{"type":["string","null"]},"description":{"type":["string","null"]},"stars":{"type":"integer","minimum":0},"forks":{"type":"integer","minimum":0},"language":{"type":["string","null"]},"license":{"type":["string","null"]},"pushedAt":{"type":["string","null"]},"discoveryScore":{"type":"number","minimum":0,"maximum":100},"matchedTargets":{"type":"array","minItems":1,"items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Matched Target","type":"object","required":["kind","target","priority"],"properties":{"kind":{"type":"string","minLength":1},"target":{"type":"string","minLength":1},"priority":{"type":"number","minimum":0}},"additionalProperties":false}},"topics":{"type":"array","items":{"type":"string"}},"watchers":{"type":"integer","minimum":0},"size":{"type":["integer","null"],"minimum":0},"openIssues":{"type":"integer","minimum":0},"createdAt":{"type":["string","null"]},"homepage":{"type":["string","null"]},"hasDiscussions":{"type":"boolean"},"latestRelease":{"type":["object","null"]},"contributors":{"type":["integer","null"],"minimum":0},"metadataStale":{"type":"boolean"},"staleEndpoints":{"type":"array","items":{"type":"string"}},"enrichmentError":{"type":"string"}},"additionalProperties":true}},"errors":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Error","type":"object","required":["target","error"],"properties":{"target":{"type":"string","minLength":1},"error":{"type":"string","minLength":1}},"additionalProperties":false}},"staleSources":{"type":"array","items":{"type":"object"}},"cacheStats":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Cache Stats","type":"object","required":["logicalRequests","freshCacheHits","notModifiedHits","staleFallbacks","networkFetches","apiCallAvoidanceRate","bodyReuseRate"],"properties":{"logicalRequests":{"type":"integer","minimum":0},"freshCacheHits":{"type":"integer","minimum":0},"notModifiedHits":{"type":"integer","minimum":0},"staleFallbacks":{"type":"integer","minimum":0},"networkFetches":{"type":"integer","minimum":0},"apiCallAvoidanceRate":{"type":"number","minimum":0,"maximum":1},"bodyReuseRate":{"type":"number","minimum":0,"maximum":1}},"additionalProperties":true}},"additionalProperties":false}
```

## File: discovery-evaluated.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Evaluated Discovery Candidates","type":"object","required":["candidates","counts","repositories","errors"],"properties":{"candidates":{"type":"integer","minimum":0},"counts":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Evaluation Counts","type":"object","required":["accept","review","reject"],"properties":{"accept":{"type":"integer","minimum":0},"review":{"type":"integer","minimum":0},"reject":{"type":"integer","minimum":0}},"additionalProperties":false},"repositories":{"type":"array","items":{"type":"object","required":["repo","evaluationScore","decision","scoreBreakdown","evaluationConfidence","reasons"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"url":{"type":["string","null"]},"description":{"type":["string","null"]},"stars":{"type":"integer","minimum":0},"forks":{"type":"integer","minimum":0},"language":{"type":["string","null"]},"license":{"type":["string","null"]},"pushedAt":{"type":["string","null"]},"discoveryScore":{"type":"number","minimum":0,"maximum":100},"matchedTargets":{"type":"array","minItems":1,"items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Matched Target","type":"object","required":["kind","target","priority"],"properties":{"kind":{"type":"string","minLength":1},"target":{"type":"string","minLength":1},"priority":{"type":"number","minimum":0}},"additionalProperties":false}},"topics":{"type":"array","items":{"type":"string"}},"watchers":{"type":"integer","minimum":0},"size":{"type":["integer","null"],"minimum":0},"openIssues":{"type":"integer","minimum":0},"createdAt":{"type":["string","null"]},"homepage":{"type":["string","null"]},"hasDiscussions":{"type":"boolean"},"latestRelease":{"type":["object","null"]},"contributors":{"type":["integer","null"],"minimum":0},"metadataStale":{"type":"boolean"},"staleEndpoints":{"type":"array","items":{"type":"string"}},"enrichmentError":{"type":"string"},"evaluationScore":{"type":"number","minimum":0,"maximum":100},"decision":{"enum":["accept","review","reject"]},"ageDays":{"type":["integer","null"],"minimum":0},"repositoryAgeDays":{"type":["integer","null"],"minimum":0},"releaseAgeDays":{"type":["integer","null"],"minimum":0},"textFit":{"type":"number","minimum":0,"maximum":1},"openIssueRatio":{"type":["number","null"],"minimum":0},"scoreBreakdown":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Evaluation Score Breakdown","type":"object","required":["fit","activity","adoption","maturity","maintenance"],"properties":{"fit":{"type":"number","minimum":0,"maximum":100},"activity":{"type":"number","minimum":0,"maximum":100},"adoption":{"type":"number","minimum":0,"maximum":100},"maturity":{"type":"number","minimum":0,"maximum":100},"maintenance":{"type":"number","minimum":0,"maximum":100}},"additionalProperties":false},"evaluationConfidence":{"enum":["low","medium","high"]},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":true}},"errors":{"type":"array"},"suppressedUnchanged":{"type":"integer","minimum":0}},"additionalProperties":false}
```

## File: discovery-memory.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Memory","type":"object","required":["schemaVersion","candidates"],"properties":{"schemaVersion":{"type":"integer","const":1},"candidates":{"type":"object","additionalProperties":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Memory Entry","type":"object","required":["fingerprint","lastSeenAt"],"properties":{"fingerprint":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Candidate Fingerprint","type":"object","required":["decision","score","stars","pushedAt","targets"],"properties":{"decision":{"enum":["accept","review","reject"]},"score":{"type":"number","minimum":0,"maximum":100},"stars":{"type":"integer","minimum":0},"pushedAt":{"type":["string","null"]},"targets":{"type":"array","items":{"type":"array","minItems":2,"maxItems":2}}},"additionalProperties":false},"lastSeenAt":{"type":"string","minLength":1}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: discovery-watchlist.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Watchlist","type":"object","required":["items","watchlist"],"properties":{"items":{"type":"integer","minimum":0},"watchlist":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Discovery Watch Item","type":"object","required":["kind","target","priority","query","reason"],"properties":{"kind":{"enum":["domain","capability","quality"]},"target":{"type":"string","minLength":1},"priority":{"type":"number","minimum":0},"query":{"type":"string","minLength":1},"reason":{"type":"string","minLength":1}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: github-id-backfill-report.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Permanent GitHub Repository ID Backfill Report",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "mode",
    "catalogSize",
    "previouslyVerified",
    "missingBefore",
    "checked",
    "assigned",
    "missingAfter",
    "complete",
    "unresolved"
  ],
  "properties": {
    "mode": {
      "enum": [
        "online",
        "offline"
      ]
    },
    "catalogSize": {
      "type": "integer",
      "minimum": 0
    },
    "previouslyVerified": {
      "type": "integer",
      "minimum": 0
    },
    "missingBefore": {
      "type": "integer",
      "minimum": 0
    },
    "checked": {
      "type": "integer",
      "minimum": 0
    },
    "assigned": {
      "type": "integer",
      "minimum": 0
    },
    "missingAfter": {
      "type": "integer",
      "minimum": 0
    },
    "complete": {
      "type": "boolean"
    },
    "unresolved": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "repo",
          "reason"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
          },
          "reason": {
            "enum": [
              "not-found",
              "renamed-or-transferred",
              "invalid-or-private",
              "identity-conflict"
            ]
          }
        }
      }
    },
    "error": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

## File: health-drift.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Drift","type":"object","required":["dropThreshold","findings","repositories"],"properties":{"dropThreshold":{"type":"number","minimum":0},"findings":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Drift Finding","type":"object","required":["repo","previousScore","currentScore","delta","previousStatus","currentStatus"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"previousScore":{"type":"number","minimum":0,"maximum":100},"currentScore":{"type":"number","minimum":0,"maximum":100},"delta":{"type":"number"},"previousStatus":{"type":"string","minLength":1},"currentStatus":{"type":"string","minLength":1}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: health-snapshot.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Snapshot","type":"object","required":["repositories"],"properties":{"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository Health","type":"object","required":["repo","score","status","reasons"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"enum":["unknown","inactive","healthy","watch","weak"]},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: health-trends.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trends","type":"object","required":["repositories"],"properties":{"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository Trend","type":"object","required":["repo","trend","week","fourWeeks","full"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"trend":{"enum":["stable","declining","improving","growing"]},"week":{"type":["object","null"],"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trend Window","required":["points","days","healthDelta","starsDelta","forksDelta","starsPerWeek","forksPerWeek"],"properties":{"points":{"type":"integer","minimum":2},"days":{"type":"integer","minimum":1},"healthDelta":{"type":["number","null"]},"starsDelta":{"type":["number","null"]},"forksDelta":{"type":["number","null"]},"starsPerWeek":{"type":["number","null"]},"forksPerWeek":{"type":["number","null"]}},"additionalProperties":false},"fourWeeks":{"type":["object","null"],"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trend Window","required":["points","days","healthDelta","starsDelta","forksDelta","starsPerWeek","forksPerWeek"],"properties":{"points":{"type":"integer","minimum":2},"days":{"type":"integer","minimum":1},"healthDelta":{"type":["number","null"]},"starsDelta":{"type":["number","null"]},"forksDelta":{"type":["number","null"]},"starsPerWeek":{"type":["number","null"]},"forksPerWeek":{"type":["number","null"]}},"additionalProperties":false},"full":{"type":["object","null"],"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Health Trend Window","required":["points","days","healthDelta","starsDelta","forksDelta","starsPerWeek","forksPerWeek"],"properties":{"points":{"type":"integer","minimum":2},"days":{"type":"integer","minimum":1},"healthDelta":{"type":["number","null"]},"starsDelta":{"type":["number","null"]},"forksDelta":{"type":["number","null"]},"starsPerWeek":{"type":["number","null"]},"forksPerWeek":{"type":["number","null"]}},"additionalProperties":false}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: history.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository History","type":"object","required":["schemaVersion","repositories"],"properties":{"schemaVersion":{"type":"integer","const":1},"repositories":{"type":"object","additionalProperties":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Repository History Point","type":"object","required":["date","health","status","stars","forks"],"properties":{"date":{"type":"string","pattern":"^\\d{4}-\\d{2}-\\d{2}$"},"health":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":["string","null"]},"stars":{"type":["integer","null"],"minimum":0},"forks":{"type":["integer","null"],"minimum":0}},"additionalProperties":false}}}},"additionalProperties":false}
```

## File: metadata-evidence.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List evidence audit",
  "type": "object",
  "required": [
    "generatedAt",
    "catalogSize",
    "uncertainEntries",
    "selected",
    "inspected",
    "counts",
    "results",
    "updates",
    "errors",
    "batchIndex",
    "wroteCatalog"
  ],
  "properties": {
    "generatedAt": {
      "type": "string",
      "minLength": 1
    },
    "catalogSize": {
      "type": "integer",
      "minimum": 0
    },
    "uncertainEntries": {
      "type": "integer",
      "minimum": 0
    },
    "selected": {
      "type": "integer",
      "minimum": 0
    },
    "inspected": {
      "type": "integer",
      "minimum": 0
    },
    "batchIndex": {
      "type": "integer",
      "minimum": 0
    },
    "wroteCatalog": {
      "type": "boolean"
    },
    "counts": {
      "type": "object",
      "required": [
        "verifiedRootLicenses",
        "githubClaimsOnly",
        "hostingCandidates",
        "proposedLicenseUpdates",
        "appliedUpdates",
        "errors",
        "scopedLicenses"
      ],
      "properties": {
        "verifiedRootLicenses": {
          "type": "integer",
          "minimum": 0
        },
        "githubClaimsOnly": {
          "type": "integer",
          "minimum": 0
        },
        "hostingCandidates": {
          "type": "integer",
          "minimum": 0
        },
        "proposedLicenseUpdates": {
          "type": "integer",
          "minimum": 0
        },
        "appliedUpdates": {
          "type": "integer",
          "minimum": 0
        },
        "errors": {
          "type": "integer",
          "minimum": 0
        },
        "scopedLicenses": {
          "type": "integer",
          "minimum": 0
        }
      },
      "additionalProperties": false
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repository",
          "repositoryId",
          "defaultBranch",
          "license",
          "hosting",
          "proposedLicense"
        ],
        "properties": {
          "repository": {
            "type": "string",
            "pattern": "^[^/]+/[^/]+$"
          },
          "repositoryId": {
            "type": "integer",
            "minimum": 1
          },
          "defaultBranch": {
            "type": "string",
            "minLength": 1
          },
          "proposedLicense": {
            "type": [
              "string",
              "null"
            ]
          },
          "license": {
            "type": "object",
            "required": [
              "status",
              "value",
              "evidence"
            ],
            "properties": {
              "status": {
                "enum": [
                  "unverified",
                  "verified-root-file",
                  "github-claim-only",
                  "conflict",
                  "scoped-licensing-review"
                ]
              },
              "value": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "method",
                    "value",
                    "url"
                  ],
                  "properties": {
                    "method": {
                      "enum": [
                        "github-repository-spdx",
                        "root-license-signature",
                        "root-license-scope-warning"
                      ]
                    },
                    "value": {
                      "type": "string"
                    },
                    "path": {
                      "type": "string"
                    },
                    "blobSha": {
                      "type": "string",
                      "pattern": "^[a-f0-9]{40}$"
                    },
                    "url": {
                      "type": "string",
                      "pattern": "^https://api.github.com/repos/"
                    }
                  },
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "hosting": {
            "type": "object",
            "required": [
              "status",
              "evidence"
            ],
            "properties": {
              "status": {
                "enum": [
                  "unverified",
                  "deployment-file-present-review-required"
                ]
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": [
                    "method",
                    "path",
                    "blobSha",
                    "url"
                  ],
                  "properties": {
                    "method": {
                      "const": "compose-root-file"
                    },
                    "path": {
                      "type": "string"
                    },
                    "blobSha": {
                      "type": "string",
                      "pattern": "^[a-f0-9]{40}$"
                    },
                    "url": {
                      "type": "string",
                      "pattern": "^https://api.github.com/repos/"
                    }
                  },
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          }
        },
        "additionalProperties": false
      }
    },
    "updates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repository",
          "license",
          "evidence"
        ],
        "properties": {
          "repository": {
            "type": "string"
          },
          "license": {
            "type": "string"
          },
          "evidence": {
            "type": "string",
            "pattern": "^https://api.github.com/repos/"
          }
        },
        "additionalProperties": false
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repository",
          "error"
        ],
        "properties": {
          "repository": {
            "type": "string"
          },
          "error": {
            "type": "string"
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

## File: readme-domain-evidence.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List reviewed upstream README evidence",
  "type": "object",
  "required": [
    "schemaVersion",
    "sourceType",
    "sources"
  ],
  "properties": {
    "schemaVersion": {
      "const": 1
    },
    "sourceType": {
      "const": "reviewed-readme-blob"
    },
    "sources": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "repository",
          "githubRepositoryId",
          "path",
          "blobSha",
          "advisoryDomains",
          "taskTerms",
          "evidenceSnippet",
          "reviewNotes"
        ],
        "properties": {
          "repository": {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$"
          },
          "githubRepositoryId": {
            "type": "integer",
            "minimum": 1
          },
          "path": {
            "const": "README.md"
          },
          "blobSha": {
            "type": "string",
            "pattern": "^[a-f0-9]{40}$"
          },
          "advisoryDomains": {
            "type": "array",
            "minItems": 1,
            "maxItems": 4,
            "uniqueItems": true,
            "items": {
              "enum": [
                "ai_media",
                "ai_agents",
                "data_ml",
                "graphics",
                "game_dev",
                "marketing",
                "software_engineering",
                "writing",
                "productivity",
                "backend",
                "web_frontend",
                "embedded_iot",
                "education",
                "cybersecurity",
                "ai_memory",
                "devops"
              ]
            }
          },
          "taskTerms": {
            "type": "array",
            "minItems": 1,
            "maxItems": 10,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "pattern": "^[a-z0-9-]+$"
            }
          },
          "evidenceSnippet": {
            "type": "string",
            "minLength": 3
          },
          "reviewNotes": {
            "type": "string",
            "minLength": 5
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

## File: replacement-report.schema.json
```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Report","type":"object","required":["threshold","findings","repositories"],"properties":{"threshold":{"type":"number","minimum":0,"maximum":100},"findings":{"type":"integer","minimum":0},"repositories":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Finding","type":"object","required":["repo","health","qualityScore","domain","suggestedReplacements"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"health":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Embedded Health","type":"object","required":["score","status","reasons"],"properties":{"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":"string","minLength":1},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"qualityScore":{"type":["number","null"]},"domain":{"type":["string","null"]},"suggestedReplacements":{"type":"array","items":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Replacement Candidate","type":"object","required":["repo","replacementScore","health","qualityScore","domain"],"properties":{"repo":{"type":"string","pattern":"^[^/\\s]+/[^/\\s]+$"},"replacementScore":{"type":"number","minimum":0},"health":{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Embedded Health","type":"object","required":["score","status","reasons"],"properties":{"score":{"type":["number","null"],"minimum":0,"maximum":100},"status":{"type":"string","minLength":1},"ageDays":{"type":["integer","null"],"minimum":0},"reasons":{"type":"array","items":{"type":"string"}}},"additionalProperties":false},"qualityScore":{"type":["number","null"]},"domain":{"type":["string","null"]}},"additionalProperties":false}}},"additionalProperties":false}}},"additionalProperties":false}
```

## File: star-sync-report.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Public GitHub Stars review report",
  "type": "object",
  "required": [
    "schemaVersion",
    "username",
    "checkedAt",
    "source",
    "summary",
    "newRepositories"
  ],
  "properties": {
    "schemaVersion": {
      "type": "integer",
      "const": 1
    },
    "username": {
      "type": "string",
      "minLength": 1
    },
    "checkedAt": {
      "type": "string",
      "minLength": 10
    },
    "source": {
      "type": "string",
      "minLength": 1
    },
    "summary": {
      "type": "object",
      "required": [
        "starred",
        "alreadyCataloged",
        "new",
        "pages",
        "duplicateApiItems"
      ],
      "properties": {
        "starred": {
          "type": "integer",
          "minimum": 0
        },
        "alreadyCataloged": {
          "type": "integer",
          "minimum": 0
        },
        "new": {
          "type": "integer",
          "minimum": 0
        },
        "pages": {
          "type": "integer",
          "minimum": 0
        },
        "duplicateApiItems": {
          "type": "integer",
          "minimum": 0
        }
      },
      "additionalProperties": false
    },
    "newRepositories": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "repo",
          "url",
          "stars",
          "language",
          "license",
          "archived",
          "disabled",
          "pushedAt"
        ],
        "properties": {
          "repo": {
            "type": "string",
            "pattern": "^[^/]+/[^/]+$"
          },
          "url": {
            "type": "string",
            "pattern": "^https://github[.]com/"
          },
          "stars": {
            "type": [
              "integer",
              "null"
            ],
            "minimum": 0
          },
          "language": {
            "type": [
              "string",
              "null"
            ]
          },
          "license": {
            "type": [
              "string",
              "null"
            ]
          },
          "archived": {
            "type": "boolean"
          },
          "disabled": {
            "type": "boolean"
          },
          "pushedAt": {
            "type": [
              "string",
              "null"
            ]
          },
          "githubRepositoryId": {
            "type": [
              "integer",
              "null"
            ],
            "minimum": 1
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```

## File: websites.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Star List Curated Website Resources",
  "type": "object",
  "required": [
    "schemaVersion",
    "websites"
  ],
  "additionalProperties": false,
  "properties": {
    "schemaVersion": {
      "type": "integer",
      "const": 1
    },
    "description": {
      "type": "string",
      "minLength": 1
    },
    "websites": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "name",
          "url",
          "type",
          "access",
          "domains",
          "tags",
          "bestFor",
          "reuse",
          "caution"
        ],
        "additionalProperties": false,
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"
          },
          "name": {
            "type": "string",
            "minLength": 2
          },
          "url": {
            "type": "string",
            "pattern": "^https://[^/\\s?#]+/?(?:[^\\s]*)?$"
          },
          "originalUrl": {
            "type": "string",
            "pattern": "^https://[^/\\s?#]+/?(?:[^\\s]*)?$"
          },
          "type": {
            "enum": [
              "inspiration-gallery",
              "motion-gallery",
              "component-marketplace",
              "component-library",
              "prompt-template-library",
              "framework-docs",
              "shader-gallery",
              "hosted-builder",
              "agent-skills-directory",
              "mcp-service",
              "npc-platform",
              "narrative-platform",
              "game-design-service",
              "asset-generator",
              "game-testing-service",
              "model-collection",
              "model-checkpoint",
              "model-hub",
              "marketing-automation-service",
              "animation-reference-library",
              "film-stills-library",
              "3d-pose-reference-tool",
              "costume-history-atlas",
              "ai-media-generator",
              "3d-asset-dataset",
              "codebase-prompt-generator",
              "pixel-vfx-editor"
            ]
          },
          "access": {
            "enum": [
              "free",
              "freemium",
              "paid",
              "unknown"
            ]
          },
          "domains": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "enum": [
                "web_frontend",
                "graphics",
                "mobile",
                "game_dev",
                "software_engineering",
                "ai_agents",
                "ai_media",
                "other",
                "marketing",
                "writing"
              ]
            }
          },
          "tags": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "minLength": 2
            }
          },
          "bestFor": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "minLength": 3
            }
          },
          "reuse": {
            "enum": [
              "reference-only",
              "license-per-item",
              "licensed-material",
              "open-source-upstream",
              "hosted-service"
            ]
          },
          "caution": {
            "type": "string",
            "minLength": 10
          },
          "mcpEndpoint": {
            "type": "string",
            "pattern": "^https://[^/\\s?#]+/mcp$"
          },
          "portfolioBaselineDomains": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "enum": [
                "web_frontend",
                "graphics",
                "mobile",
                "game_dev",
                "software_engineering",
                "ai_agents",
                "ai_media",
                "other",
                "marketing",
                "writing"
              ]
            }
          },
          "portfolioRequiredSignals": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "minLength": 2
            }
          },
          "sourceLicenseTag": {
            "type": "string",
            "minLength": 2
          },
          "upstreamModel": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
          },
          "safetyRisk": {
            "enum": [
              "reduced-refusal",
              "unknown",
              "standard"
            ]
          },
          "supportedLanguages": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "items": {
              "type": "string",
              "pattern": "^[a-z]{2}(?:-[A-Z]{2})?$"
            }
          }
        }
      }
    }
  }
}
```
