import { useState } from 'react'

const LoanApplication = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    applicant_name: '',
    loan_amount: '',
    income: '',
    employment_status: 'employed',
    credit_score: '',
    purpose: 'home_purchase'
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    try {
      await onSubmit({
        ...formData,
        loan_amount: parseFloat(formData.loan_amount),
        income: parseFloat(formData.income),
        credit_score: formData.credit_score ? parseInt(formData.credit_score) : null
      })
      
      // Reset form
      setFormData({
        applicant_name: '',
        loan_amount: '',
        income: '',
        employment_status: 'employed',
        credit_score: '',
        purpose: 'home_purchase'
      })
    } catch (error) {
      console.error('Error submitting application:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto bg-white shadow rounded-lg p-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="applicant_name" className="block text-sm font-medium text-gray-700">
            Full Name
          </label>
          <input
            type="text"
            name="applicant_name"
            id="applicant_name"
            required
            value={formData.applicant_name}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <div>
          <label htmlFor="loan_amount" className="block text-sm font-medium text-gray-700">
            Loan Amount ($)
          </label>
          <input
            type="number"
            name="loan_amount"
            id="loan_amount"
            required
            min="0"
            step="0.01"
            value={formData.loan_amount}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <div>
          <label htmlFor="income" className="block text-sm font-medium text-gray-700">
            Annual Income ($)
          </label>
          <input
            type="number"
            name="income"
            id="income"
            required
            min="0"
            step="0.01"
            value={formData.income}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <div>
          <label htmlFor="employment_status" className="block text-sm font-medium text-gray-700">
            Employment Status
          </label>
          <select
            name="employment_status"
            id="employment_status"
            value={formData.employment_status}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
          >
            <option value="employed">Employed</option>
            <option value="self_employed">Self Employed</option>
            <option value="unemployed">Unemployed</option>
            <option value="retired">Retired</option>
          </select>
        </div>

        <div>
          <label htmlFor="credit_score" className="block text-sm font-medium text-gray-700">
            Credit Score (Optional)
          </label>
          <input
            type="number"
            name="credit_score"
            id="credit_score"
            min="300"
            max="850"
            value={formData.credit_score}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <div>
          <label htmlFor="purpose" className="block text-sm font-medium text-gray-700">
            Loan Purpose
          </label>
          <select
            name="purpose"
            id="purpose"
            value={formData.purpose}
            onChange={handleChange}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm px-3 py-2 border"
          >
            <option value="home_purchase">Home Purchase</option>
            <option value="refinance">Refinance</option>
            <option value="debt_consolidation">Debt Consolidation</option>
            <option value="home_improvement">Home Improvement</option>
            <option value="business">Business</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Application'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default LoanApplication
