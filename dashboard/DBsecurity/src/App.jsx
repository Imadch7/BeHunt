import React, { useState } from 'react';
import { Shield,Syringe, AlertTriangle, CheckCircle, Upload, FileText, Clock, Target, Activity, Server, AlertCircle, Info, Code } from 'lucide-react';

const SecurityDashboard = () => {
  const [testData, setTestData] = useState({
    scan_metadata: {
      scan_id: "scan_001",
      target_domain: "testphp.vulnweb.com",
      scan_date: "2024-11-15T10:30:00Z",
      scanner_version: "1.0",
      authorization: "written_permission.pdf"
    },
    all_responses: [
      {
        test_id: "sqli_001",
        test_type: "SQL Injection",
        payload_type: "OR-based boolean",
        target_url: "http://testphp.vulnweb.com?searchFor=\"' or 3=3 --\"",
        status: 200,
        response_time_ms: 245,
        response_size_bytes: 4532,
        headers: {
          "content-type": "text/html",
          "server": "nginx"
        },
        vulnerability_indicators: {
          sql_errors: false,
          unusual_response_size: false,
          response_time_anomaly: false
        },
        severity: "medium",
        confirmed: false,
        notes: "Requires manual verification"
      }
    ]
  });

  const [selectedTest, setSelectedTest] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result);
          setTestData(json);
          setSelectedTest(null);
          setError('');
        } catch (error) {
          setError('Invalid JSON file: ' + error.message);
        }
      };
      reader.readAsText(file);
    }
  };

  const handleUrlSubmit = async () => {
    if (!targetUrl.trim()) {
      setError('Please enter a target URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Extract domain from URL for filename
      const urlObj = new URL(targetUrl);
      const domain = urlObj.hostname.replace(/\./g, '_');
      const filename = `${domain}_response.json`;
      
      // Try to fetch from /output/ directory
      const response = await fetch(`/output/${filename}`);
      
      if (!response.ok) {
        throw new Error(`File not found: ${filename}. Make sure the scan has been completed.`);
      }

      const json = await response.json();
      setTestData(json);
      setSelectedTest(null);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to load scan results. Check if the file exists in /output/');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'critical': return 'bg-red-600 text-white border-red-700';
      case 'high': return 'bg-red-100 text-red-800 border-red-300';
      case 'medium': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'low': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'info': return 'bg-blue-100 text-blue-800 border-blue-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getStatusColor = (status) => {
    if (status >= 200 && status < 300) return 'text-green-500';
    if (status >= 400 && status < 500) return 'text-orange-500';
    if (status >= 500) return 'text-red-500';
    return 'text-gray-500';
  };

  const formatBytes = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  };

  const formatDate = (dateStr) => {
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr;
    }
  };

  const stats = {
    total: testData.all_responses?.length || 0,
    critical: testData.all_responses?.filter(r => r.severity?.toLowerCase() === 'critical').length || 0,
    high: testData.all_responses?.filter(r => r.severity?.toLowerCase() === 'high').length || 0,
    medium: testData.all_responses?.filter(r => r.severity?.toLowerCase() === 'medium').length || 0,
    low: testData.all_responses?.filter(r => r.severity?.toLowerCase() === 'low').length || 0,
    confirmed: testData.all_responses?.filter(r => r.confirmed === true).length || 0,
    withIndicators: testData.all_responses?.filter(r => 
      r.vulnerability_indicators?.sql_errors || 
      r.vulnerability_indicators?.unusual_response_size || 
      r.vulnerability_indicators?.response_time_anomaly
    ).length || 0
  };

  const testTypes = [...new Set(testData.all_responses?.map(r => r.test_type) || [])];
  const hasData = testData.all_responses && testData.all_responses.length > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          {/* Enhanced Header with Branding */}
          <div className="bg-gradient-to-r from-slate-800 via-cyan-900/30 to-slate-800 border border-cyan-700/50 rounded-2xl p-6 mb-6">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center gap-4">
                <div className="relative">
                  <div className="absolute inset-0 bg-cyan-500/20 blur-xl rounded-full"></div>
                  <img src='/public/379509_hacker_icon.png' className="w-25 h-25 p-0 m-0 text-cyan-400 relative z-10" />
                </div>
                <div>
                  <h1 className="text-4xl font-bold text-white mb-1 flex items-center gap-3">
                    BeHunt
                    <span className="text-sm font-normal px-3 py-1 bg-cyan-600/30 text-cyan-300 rounded-full border border-cyan-500/50">
                      v1.0
                    </span>
                  </h1>
                  <p className="text-cyan-400 text-sm font-medium mb-1">Security Testing Dashboard</p>
                  <p className="text-slate-400 text-xs">Open-source web vulnerability analysis tool</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <a 
                  href="https://github.com/Imadch7/BeHunt" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition border border-slate-600"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                  <span className="text-sm font-medium">GitHub</span>
                </a>
                <label className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg cursor-pointer transition shadow-lg shadow-cyan-900/50">
                  <Upload className="w-4 h-4" />
                  <span className="text-sm font-medium">Upload JSON</span>
                  <input type="file" accept=".json" onChange={handleFileUpload} className="hidden" />
                </label>
              </div>
            </div>

            {/* Feature Tags */}
            <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-slate-700/50">
              <span className="px-3 py-1 bg-blue-900/30 text-blue-300 rounded-full text-xs font-medium border border-blue-700/50 flex items-center gap-1">
                <Target className="w-3 h-3" />
                Subdomain Enum
              </span>
              <span className="px-3 py-1 bg-red-900/30 text-red-300 rounded-full text-xs font-medium border border-red-700/50 flex items-center gap-1">
              <Syringe className="w-3 h-3" />
                SQLi Detection
              </span>
              <span className="px-3 py-1 bg-orange-900/30 text-orange-300 rounded-full text-xs font-medium border border-orange-700/50 flex items-center gap-1">
                <Code className="w-3 h-3" />
                XSS Scanning
              </span>
              <span className="px-3 py-1 bg-purple-900/30 text-purple-300 rounded-full text-xs font-medium border border-purple-700/50 flex items-center gap-1">
                <FileText className="w-3 h-3" />
                LFI Testing
              </span>
              <span className="px-3 py-1 bg-green-900/30 text-green-300 rounded-full text-xs font-medium border border-green-700/50 flex items-center gap-1">
                <CheckCircle className="w-3 h-3" />
                Multiple Output Formats
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div>
                                  <h1 className="text-3xl font-bold text-white">Security Testing Dashboard</h1>
                <p className="text-slate-400 text-sm">Ethical Penetration Testing Results</p>
              </div>
            </div>
            
          </div>

          {/* Scan Metadata */}
          {testData.scan_metadata && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 grid grid-cols-2 md:grid-cols-5 gap-4">
              <div>
                <p className="text-xs text-slate-500 mb-1">Scan ID</p>
                <p className="text-sm text-white font-mono">{testData.scan_metadata.scan_id}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Target Domain</p>
                <p className="text-sm text-cyan-400 font-medium">{testData.scan_metadata.target_domain}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Scan Date</p>
                <p className="text-sm text-white">{formatDate(testData.scan_metadata.scan_date)}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Scanner Version</p>
                <p className="text-sm text-white">{testData.scan_metadata.scanner_version}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Authorization</p>
                <p className="text-sm text-green-400 flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" />
                  {testData.scan_metadata.authorization}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium">Total Tests</p>
              <Target className="w-5 h-5 text-blue-400" />
            </div>
            <p className="text-2xl font-bold text-white">{stats.total}</p>
          </div>

          <div className="bg-slate-800 border border-red-900/30 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium">Critical</p>
              <AlertTriangle className="w-5 h-5 text-red-500" />
            </div>
            <p className="text-2xl font-bold text-red-400">{stats.critical}</p>
          </div>

          <div className="bg-slate-800 border border-orange-900/30 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium">High</p>
              <AlertCircle className="w-5 h-5 text-orange-500" />
            </div>
            <p className="text-2xl font-bold text-orange-400">{stats.high}</p>
          </div>

          <div className="bg-slate-800 border border-yellow-900/30 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium">Medium</p>
              <Info className="w-5 h-5 text-yellow-500" />
            </div>
            <p className="text-2xl font-bold text-yellow-400">{stats.medium}</p>
          </div>

          <div className="bg-slate-800 border border-green-900/30 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium">Confirmed</p>
              <CheckCircle className="w-5 h-5 text-green-500" />
            </div>
            <p className="text-2xl font-bold text-green-400">{stats.confirmed}</p>
          </div>

          <div className="bg-slate-800 border border-purple-900/30 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium">Indicators</p>
              <Activity className="w-5 h-5 text-purple-500" />
            </div>
            <p className="text-2xl font-bold text-purple-400">{stats.withIndicators}</p>
          </div>
        </div>

        {/* Test Types Summary */}
        {testTypes.length > 0 && (
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 mb-8">
            <h3 className="text-lg font-bold text-white mb-4">Test Types</h3>
            <div className="flex flex-wrap gap-2">
              {testTypes.map((type, idx) => (
                <span key={idx} className="px-3 py-1 bg-slate-700 text-cyan-300 rounded-full text-sm font-medium">
                  {type}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Results Table */}
        <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden mb-6">
          <div className="p-6 border-b border-slate-700">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-cyan-400" />
              Detailed Test Results
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-900">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Test ID</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Type</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Payload</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Time</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Size</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Severity</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Confirmed</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {testData.all_responses?.map((response, index) => (
                  <tr key={index} className="hover:bg-slate-750 transition">
                    <td className="px-4 py-3 text-sm text-slate-300 font-mono">{response.test_id}</td>
                    <td className="px-4 py-3 text-sm text-slate-300">{response.test_type}</td>
                    <td className="px-4 py-3 text-xs text-slate-400 max-w-xs truncate" title={response.payload_type}>
                      {response.payload_type}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`text-sm font-bold ${getStatusColor(response.status)}`}>
                        {response.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-300">{response.response_time_ms.toFixed(3)}ms</td>
                    <td className="px-4 py-3 text-sm text-slate-300">{formatBytes(response.response_size_bytes)}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold border ${getSeverityColor(response.severity)}`}>
                        {response.severity?.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      {response.confirmed ? (
                        <CheckCircle className="w-5 h-5 text-green-400" />
                      ) : (
                        <Clock className="w-5 h-5 text-slate-600" />
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => setSelectedTest(response)}
                        className="px-3 py-1 bg-cyan-600 hover:bg-cyan-700 text-white text-xs rounded transition"
                      >
                        Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Detail Modal */}
        {selectedTest && (
          <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50" onClick={() => setSelectedTest(null)}>
            <div className="bg-slate-800 border border-slate-700 rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
              <div className="p-6 border-b border-slate-700 flex items-center justify-between">
                <h3 className="text-xl font-bold text-white">Test Details: {selectedTest.test_id}</h3>
                <button onClick={() => setSelectedTest(null)} className="text-slate-400 hover:text-white">✕</button>
              </div>
              
              <div className="p-6 space-y-4">
                <div>
                  <p className="text-xs text-slate-500 mb-1">Target URL</p>
                  <p className="text-sm text-cyan-400 font-mono break-all">{selectedTest.target_url}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Test Type</p>
                    <p className="text-sm text-white">{selectedTest.test_type}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Payload Type</p>
                    <p className="text-sm text-white">{selectedTest.payload_type}</p>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Status Code</p>
                    <p className={`text-sm font-bold ${getStatusColor(selectedTest.status)}`}>{selectedTest.status}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Response Time</p>
                    <p className="text-sm text-white">{selectedTest.response_time_ms.toFixed(3)}ms</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Response Size</p>
                    <p className="text-sm text-white">{formatBytes(selectedTest.response_size_bytes)}</p>
                  </div>
                </div>

                {selectedTest.headers && (
                  <div>
                    <p className="text-xs text-slate-500 mb-2">Response Headers</p>
                    <div className="bg-slate-900 rounded p-3 space-y-1">
                      {Object.entries(selectedTest.headers).map(([key, value]) => (
                        <div key={key} className="flex items-start gap-2">
                          <Server className="w-3 h-3 text-slate-600 mt-0.5" />
                          <span className="text-xs text-slate-400 font-mono">{key}:</span>
                          <span className="text-xs text-slate-300 font-mono">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {selectedTest.vulnerability_indicators && (
                  <div>
                    <p className="text-xs text-slate-500 mb-2">Vulnerability Indicators</p>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        {selectedTest.vulnerability_indicators.sql_errors ? 
                          <AlertTriangle className="w-4 h-4 text-red-400" /> : 
                          <CheckCircle className="w-4 h-4 text-green-400" />
                        }
                        <span className="text-sm text-slate-300">SQL Errors: {selectedTest.vulnerability_indicators.sql_errors ? 'Detected' : 'None'}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {selectedTest.vulnerability_indicators.unusual_response_size ? 
                          <AlertTriangle className="w-4 h-4 text-red-400" /> : 
                          <CheckCircle className="w-4 h-4 text-green-400" />
                        }
                        <span className="text-sm text-slate-300">Unusual Response Size: {selectedTest.vulnerability_indicators.unusual_response_size ? 'Yes' : 'No'}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {selectedTest.vulnerability_indicators.response_time_anomaly ? 
                          <AlertTriangle className="w-4 h-4 text-red-400" /> : 
                          <CheckCircle className="w-4 h-4 text-green-400" />
                        }
                        <span className="text-sm text-slate-300">Response Time Anomaly: {selectedTest.vulnerability_indicators.response_time_anomaly ? 'Yes' : 'No'}</span>
                      </div>
                    </div>
                  </div>
                )}

                {selectedTest.notes && (
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Notes</p>
                    <p className="text-sm text-slate-300 bg-slate-900 rounded p-3">{selectedTest.notes}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Enhanced Footer */}
        <div className="mt-8 space-y-4">
          {/* Main Footer */}
          <div className="bg-gradient-to-r from-slate-800 via-cyan-900/20 to-slate-800 border border-slate-700 rounded-2xl p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* About Section */}
              <div>
                <h3 className="text-white font-bold text-lg mb-3 flex items-center gap-2">
                  <Shield className="w-5 h-5 text-cyan-400" />
                  About BeHunt
                </h3>
                <p className="text-slate-400 text-sm mb-3">
                  An open-source web vulnerability analysis tool for automated security testing. 
                  Designed for ethical hackers and security professionals.
                </p>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 bg-green-900/30 text-green-300 rounded text-xs font-medium border border-green-700/50">
                    MIT License
                  </span>
                  <span className="px-2 py-1 bg-cyan-900/30 text-cyan-300 rounded text-xs font-medium border border-cyan-700/50">
                    Open Source
                  </span>
                </div>
              </div>

              {/* Quick Links */}
              <div>
                <h3 className="text-white font-bold text-lg mb-3 flex items-center gap-2">
                  <Activity className="w-5 h-5 text-cyan-400" />
                  Quick Commands
                </h3>
                <div className="space-y-2">
                  <div className="text-xs">
                    <span className="text-slate-500">For Enumeration:</span>
                    <code className="block text-cyan-400 font-mono mt-1 bg-slate-900/50 px-2 py-1 rounded">
                      behunt -u target.com -E
                    </code>
                  </div>
                  <div className="text-xs">
                    <span className="text-slate-500">SQLI Full Test:</span>
                    <code className="block text-cyan-400 font-mono mt-1 bg-slate-900/50 px-2 py-1 rounded">
                      behunt -u target.com -T 1 -w wordlist -O json
                    </code>
                  </div>
                </div>
              </div>

              {/* Resources & Links */}
              <div>
                <h3 className="text-white font-bold text-lg mb-3 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-cyan-400" />
                  Resources
                </h3>
                <div className="space-y-2">
                  <a 
                    href="https://github.com/Imadch7/BeHunt" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300 text-sm transition"
                  >
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    GitHub Repository
                  </a>
                  <a 
                    href="https://github.com/Imadch7" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300 text-sm transition"
                  >
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                    </svg>
                    Author: Imadch7
                  </a>
                  <button 
                    onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})}
                    className="flex items-center gap-2 text-slate-400 hover:text-cyan-400 text-sm transition"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                    </svg>
                    Back to Top
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Disclaimer Footer */}
          <div className="bg-red-900/20 border border-red-700/50 rounded-xl p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-red-300 font-semibold text-sm mb-1">
                  ⚠️ Important Legal Disclaimer
                </p>
                <p className="text-slate-400 text-xs">
                  This tool is intended for <strong>educational purposes and authorized security testing only</strong>. 
                  Always obtain proper written authorization before testing any web application. 
                  Unauthorized access to computer systems is illegal and punishable by law. 
                  The authors and contributors are not responsible for misuse or damage caused by this tool.
                </p>
              </div>
            </div>
          </div>

          {/* Copyright Footer */}
          <div className="text-center py-4 border-t border-slate-800">
            <p className="text-slate-500 text-sm flex items-center justify-center gap-2 flex-wrap">
              <Clock className="w-4 h-4" />
              <span>© 2024 BeHunt - All activities logged and monitored</span>
              <span className="text-slate-700">|</span>
              <span className="flex items-center gap-1">
                <CheckCircle className="w-3 h-3 text-green-500" />
                Ethical Testing Only
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SecurityDashboard;