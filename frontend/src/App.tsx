import React, { useState } from 'react';

const API_URL = 'https://tata-idea-generation-mollick.onrender.com';

type Step = 'form' | 'communication' | 'result';

interface AgentMessage {
  agent: string;
  message: string;
}

function App() {
  const [team, setTeam] = useState('HR');
  const [idea, setIdea] = useState('');
  const [conversations, setConversations] = useState<AgentMessage[]>([]);
  const [finalResult, setFinalResult] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [step, setStep] = useState<Step>('form');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setConversations([]);
    setFinalResult('');
    setIsGenerating(true);
    setStep('form');

    try {
      const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team, idea }),
      });

      const data = await response.json();

      if (data.error) {
        alert(`Error: ${data.error}`);
        setIsGenerating(false);
      } else {
        setConversations(data.conversations || []);
        setFinalResult(data.final_document || '');
        setIsGenerating(false);
        setStep('communication');
      }
    } catch (error) {
      alert(`Error: ${error}`);
      setIsGenerating(false);
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-tata-blue text-white p-4">
        <h1 className="text-3xl font-bold">Tata Communications AI Idea Generation</h1>
      </header>
      <div className="max-w-4xl mx-auto pt-4">
        <div className="flex border-b">
          <button
            className={`py-2 px-4 ${step === 'form' ? 'border-b-2 border-tata-blue' : ''}`}
            onClick={() => setStep('form')}
          >
            Idea Generation
          </button>
          <button
            className={`py-2 px-4 ${step === 'communication' ? 'border-b-2 border-tata-blue' : ''}`}
            onClick={() => setStep('communication')}
            disabled={conversations.length === 0}
          >
            Agent Conversation
          </button>
          <button
            className={`py-2 px-4 ${step === 'result' ? 'border-b-2 border-tata-blue' : ''}`}
            onClick={() => setStep('result')}
            disabled={!finalResult}
          >
            Final Document
          </button>
        </div>
      </div>
      <main className="p-8">
        {step === 'form' && (
          <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-4">New Idea</h2>
            {isGenerating ? (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-tata-blue mb-4"></div>
                <h3 className="text-xl font-semibold mb-2">AI Agents are Working...</h3>
                <p className="text-gray-600">Our team of AI agents is collaborating on your idea. This may take a few moments.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit}>
                <div className="mb-4">
                  <label htmlFor="team" className="block text-gray-700 font-bold mb-2">Select Team</label>
                  <select id="team" value={team} onChange={e => setTeam(e.target.value)} className="w-full px-3 py-2 border rounded-lg">
                    <option>HR</option>
                    <option>Marketing</option>
                    <option>Product Management</option>
                  </select>
                </div>
                <div className="mb-4">
                  <label htmlFor="idea" className="block text-gray-700 font-bold mb-2">Your Idea</label>
                  <textarea id="idea" value={idea} onChange={e => setIdea(e.target.value)} rows={4} className="w-full px-3 py-2 border rounded-lg" required></textarea>
                </div>
                <button type="submit" className="bg-tata-blue text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700">
                  Submit Idea
                </button>
              </form>
            )}
          </div>
        )}

        {step === 'communication' && (
          <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md mt-8">
            <h2 className="text-2xl font-semibold mb-4">Agent Conversation</h2>
            <div className="space-y-6 max-h-96 overflow-y-auto">
              {conversations.map((conv, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-4 border-l-4 border-tata-blue">
                  <div className="flex items-center mb-3">
                    <div className="w-8 h-8 bg-tata-blue rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                      {conv.agent.charAt(0)}
                    </div>
                    <div className="font-semibold text-tata-blue text-sm uppercase tracking-wide">
                      {conv.agent}
                    </div>
                  </div>
                  <div className="text-gray-800 leading-relaxed">
                    {conv.message.split('\n').map((line, lineIndex) => {
                      if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
                        // Bold headers
                        return (
                          <h4 key={lineIndex} className="font-semibold text-gray-900 mt-3 mb-1">
                            {line.replace(/\*\*/g, '')}
                          </h4>
                        );
                      } else if (line.trim().match(/^\d+\./)) {
                        // Numbered lists
                        return (
                          <div key={lineIndex} className="ml-4 mb-1">
                            {line}
                          </div>
                        );
                      } else if (line.trim() === '') {
                        // Empty lines for spacing
                        return <br key={lineIndex} />;
                      } else {
                        // Regular text
                        return (
                          <p key={lineIndex} className="mb-2">
                            {line}
                          </p>
                        );
                      }
                    })}
                  </div>
                </div>
              ))}
              {conversations.length === 0 && (
                <div className="text-center text-gray-500 py-8">
                  No conversation available yet.
                </div>
              )}
            </div>
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => setStep('form')}
                className="bg-gray-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-600"
              >
                Generate New Idea
              </button>
              <button
                onClick={() => setStep('result')}
                className="bg-tata-blue text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700"
                disabled={!finalResult}
              >
                View Final Document →
              </button>
            </div>
          </div>
        )}

        {step === 'result' && (
          <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md mt-8">
            <h2 className="text-2xl font-semibold mb-4">Final Document</h2>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg">{finalResult}</pre>
            </div>
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => setStep('communication')}
                className="bg-gray-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-600"
              >
                ← View Conversation
              </button>
              <button
                onClick={() => setStep('form')}
                className="bg-tata-blue text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700"
              >
                Generate New Idea
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
