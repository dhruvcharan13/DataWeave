export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            EY Data Integration MVP
          </h1>
          <p className="text-lg text-gray-600">
            Upload, analyze, and merge datasets with AI-powered suggestions
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Welcome to the Data Integration Platform
            </h2>
            <p className="text-gray-600 mb-6">
              This hackathon MVP will help you upload CSV/Excel files, analyze their schemas, 
              detect relationships, create mappings, and export merged datasets.
            </p>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="font-semibold text-blue-900 mb-2">Step 1: Upload Files</h3>
                <p className="text-blue-700 text-sm">
                  Upload your CSV/Excel files to get started with schema analysis
                </p>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg">
                <h3 className="font-semibold text-green-900 mb-2">Step 2: Analyze & Map</h3>
                <p className="text-green-700 text-sm">
                  AI will detect relationships and suggest mappings between datasets
                </p>
              </div>
              
              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-900 mb-2">Step 3: Clean Data</h3>
                <p className="text-purple-700 text-sm">
                  Review and approve AI-suggested data cleaning operations
                </p>
              </div>
              
              <div className="bg-orange-50 p-4 rounded-lg">
                <h3 className="font-semibold text-orange-900 mb-2">Step 4: Export</h3>
                <p className="text-orange-700 text-sm">
                  Generate merged datasets with complete schema documentation
                </p>
              </div>
            </div>
            
            <div className="mt-8 text-center">
              <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}