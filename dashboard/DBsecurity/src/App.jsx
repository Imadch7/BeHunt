import React, { useState } from 'react';
import { Shield, AlertTriangle, CheckCircle, Upload, FileText, Clock, Target, Activity, Server, AlertCircle, Info } from 'lucide-react';
import './index.css'

const SecurityDashboard = () => {
  const [testData, setTestData] = useState({
      
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
          } catch (error) {
            alert('Invalid JSON file: ' + error.message);
          }
        };
        reader.readAsText(file);
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
  
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Shield className="w-10 h-10 text-cyan-400" />
                <div>
                  <h1 className="text-3xl font-bold text-black">Security Testing Dashboard</h1>
                  <p className="text-slate-400 text-sm">Ethical Penetration Testing Results</p>
                </div>
              </div>
              <label className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg cursor-pointer transition">
                <Upload className="w-4 h-4" />
                <span className="text-sm font-medium">Upload JSON</span>
                <input type="file" accept=".json" onChange={handleFileUpload} className="hidden" />
              </label>
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
                      <td className="px-4 py-3 text-sm text-slate-300">{response.response_time_ms}ms</td>
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
                      <p className="text-sm text-white">{selectedTest.response_time_ms}ms</p>
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
  
          {/* Footer */}
          <div className="mt-6 p-4 bg-slate-800 border border-slate-700 rounded-lg">
            <p className="text-sm text-slate-400 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Testing authorized websites only. All activities are logged and monitored for compliance.
            </p>
          </div>
        </div>
      </div>
    );
};

export default SecurityDashboard;