import { useState, useEffect } from 'react'
import './App.css'
import LoanApplication from './components/LoanApplication'
import LoanList from './components/LoanList'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [loans, setLoans] = useState([])

  useEffect(() => {
    fetchLoans()
  }, [])

  const fetchLoans = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/loans')
      const data = await response.json()
      setLoans(data)
    } catch (error) {
      console.error('Error fetching loans:', error)
    }
  }

  const handleLoanSubmit = async (loanData) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/loans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loanData),
      })
      if (response.ok) {
        fetchLoans() // Refresh the loan list
        setActiveTab('dashboard') // Switch to dashboard
      }
    } catch (error) {
      console.error('Error submitting loan:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Loan Origination System
              </h1>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'dashboard'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveTab('apply')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'apply'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Apply for Loan
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {activeTab === 'dashboard' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Loan Applications</h2>
            <LoanList loans={loans} />
          </div>
        )}
        {activeTab === 'apply' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Apply for a Loan</h2>
            <LoanApplication onSubmit={handleLoanSubmit} />
          </div>
        )}
      </main>
    </div>
  )
}

export default App
