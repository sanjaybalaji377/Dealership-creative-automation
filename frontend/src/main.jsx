import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Download, Upload, Sparkles, LogIn, CheckCircle2, Image as ImageIcon } from 'lucide-react';
import { getAccounts, getDealerships, uploadBackground, generateCreatives, fullUrl, login } from './services/api';
import './styles.css';

const SAMPLE_IMAGES = [
    { name: 'Tata NEXON', url: '/api/assets/Sample-input-images/tata1.jpg' },
    { name: 'VW Virtus', url: '/api/assets/Sample-input-images/vw-new.jpg' },
    { name: 'VW Taigun', url: '/api/assets/Sample-input-images/vw1.jpg' },
    { name: 'Hyundai Venue', url: '/api/assets/Sample-input-images/hyundai.jpg' },
    { name: 'Generic Showroom', url: '/api/assets/Sample-input-images/brand-square.png' },
];

function App() {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));
  const [authForm, setAuthForm] = useState({ email: 'admin@dealercreative.com', password: 'Admin@123' });
  const [accounts, setAccounts] = useState([]);
  const [accountId, setAccountId] = useState('');
  const [dealerships, setDealerships] = useState([]);
  const [selectedDealers, setSelectedDealers] = useState([]);
  const [background, setBackground] = useState(null);
  const [predefinedBg, setPredefinedBg] = useState(null);
  const [includeLogo, setIncludeLogo] = useState(true);
  const [logoType, setLogoType] = useState('light');
  const [outputKeys, setOutputKeys] = useState(['instagram_square']);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!user) return;
    getAccounts().then(data => {
      setAccounts(data.accounts || []);
      if (data.accounts?.[0]) setAccountId(data.accounts[0].id);
    });
  }, [user]);

  useEffect(() => {
    if (!accountId || !user) return;
    getDealerships(accountId).then(data => {
      setDealerships(data.dealerships || []);
      setSelectedDealers([]);
    });
  }, [accountId, user]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await login(authForm.email, authForm.password);
    if (res.error) setMessage(res.error);
    else {
        localStorage.setItem('user', JSON.stringify(res.user));
        setUser(res.user);
        setMessage('');
    }
    setLoading(false);
  };

  const toggleDealer = (id) => {
    setSelectedDealers(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  };

  const toggleOutput = (key) => {
    setOutputKeys(prev => prev.includes(key) ? prev.filter(x => x !== key) : [...prev, key]);
  };

  const handleGenerate = async () => {
    setMessage('');
    setResult(null);
    if (!background && !predefinedBg) return setMessage('Upload or select a background image.');
    if (selectedDealers.length === 0) return setMessage('Select at least one dealership.');
    if (outputKeys.length === 0) return setMessage('Select at least one output format.');

    setLoading(true);
    let bgFilename = '';
    try {
      if (background) {
        console.log('Main: Uploading background...');
        const uploaded = await uploadBackground(background);
        if (uploaded.error) throw new Error(uploaded.error);
        bgFilename = uploaded.filename;
      } else if (predefinedBg) {
        bgFilename = predefinedBg.replace('/api/assets/', '');
      }
      
      console.log('Main: Generating creatives with payload:', { bgFilename, selectedDealers, outputKeys });
      const generated = await generateCreatives({
        background_filename: bgFilename,
        dealer_ids: selectedDealers,
        output_keys: outputKeys,
        include_logo: includeLogo,
        logo_type: logoType,
      });
      if (generated.error) throw new Error(generated.error);
      setResult(generated);
    } catch (err) {
      setMessage(err.message || 'Generation failed');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <div className="loginPage">
        <form className="card loginCard" onSubmit={handleLogin}>
            <h1>Login</h1>
            <p>Admin Portal - Dealership Creative Tool</p>
            <label>Email</label>
            <input type="email" value={authForm.email} onChange={e => setAuthForm({ ...authForm, email: e.target.value })} required />
            <label>Password</label>
            <input type="password" value={authForm.password} onChange={e => setAuthForm({ ...authForm, password: e.target.value })} required />
            <button className="primary" type="submit" disabled={loading}><LogIn size={20}/> {loading ? 'Logging in...' : 'Sign In'}</button>
            {message && <p className="error">{message}</p>}
        </form>
    </div>;
  }

  return <div className="app">
    <header className="hero">
      <div>
        <div className="userBadge">Welcome, {user.name} <button className="logout" onClick={() => { localStorage.clear(); setUser(null); }}>Logout</button></div>
        <h1>Dealership Creative Automation Tool</h1>
        <p>Generate brand-wise dealership creatives in bulk for Instagram formats.</p>
      </div>
      <div className="badge"><CheckCircle2 size={18}/> Automated processing enabled</div>
    </header>

    <main className="grid">
      <section className="card">
        <h2>1. Brand & Dealership</h2>
        <label>Account / Brand</label>
        <select value={accountId} onChange={e => setAccountId(e.target.value)}>
          {accounts.map(a => <option key={a.id} value={a.id}>{a.name} ({a.dealer_count})</option>)}
        </select>

        <div className="dealerTop">
          <h3>Dealerships</h3>
          <div className="groupBtns">
            <button onClick={() => setSelectedDealers(dealerships.map(d => d.id))}>Select all</button>
            <button onClick={() => setSelectedDealers([])}>Clear</button>
          </div>
        </div>
        <div className="dealerList">
          {dealerships.map(d => <label key={d.id} className={`checkRow ${selectedDealers.includes(d.id) ? 'active' : ''}`}>
            <input type="checkbox" checked={selectedDealers.includes(d.id)} onChange={() => toggleDealer(d.id)} />
            <span>{d.name}</span>
            {selectedDealers.includes(d.id) && <CheckCircle2 size={16} className="checkIcon" />}
          </label>)}
        </div>
      </section>

      <section className="card">
        <h2>2. Assets & Output</h2>
        <div className="assetToggle">
            <button className={!predefinedBg ? 'active' : ''} onClick={() => setPredefinedBg(null)}><Upload size={16}/> Upload New</button>
            <button className={predefinedBg ? 'active' : ''} onClick={() => setPredefinedBg(SAMPLE_IMAGES[0].url)}><ImageIcon size={16}/> Predefined</button>
        </div>

        {!predefinedBg ? (
            <label className="uploadBox">
                <Upload size={24}/>
                <span>{background ? background.name : 'Upload background JPG/PNG'}</span>
                <input type="file" accept="image/png,image/jpeg" onChange={e => { setBackground(e.target.files?.[0] || null); setPredefinedBg(null); }} />
            </label>
        ) : (
            <div className="sampleGallery">
                {SAMPLE_IMAGES.map(img => <img key={img.url} src={fullUrl(img.url)} className={predefinedBg === img.url ? 'selected' : ''} onClick={() => { setPredefinedBg(img.url); setBackground(null); }} title={img.name} />)}
            </div>
        )}

        <label className="checkRow mt"><input type="checkbox" checked={includeLogo} onChange={e => setIncludeLogo(e.target.checked)} /> Include dealership logo</label>
        <div className="formGroup">
            <label>Logo style</label>
            <select value={logoType} onChange={e => setLogoType(e.target.value)} disabled={!includeLogo}>
                <option value="light">Light logo</option>
                <option value="dark">Dark logo</option>
            </select>
        </div>

        <h3>Output formats</h3>
        <div className="formatGrid">
            <label className="checkRow"><input type="checkbox" checked={outputKeys.includes('instagram_square')} onChange={() => toggleOutput('instagram_square')} /> Square (1:1)</label>
            <label className="checkRow"><input type="checkbox" checked={outputKeys.includes('instagram_portrait')} onChange={() => toggleOutput('instagram_portrait')} /> Portrait (4:5)</label>
            <label className="checkRow"><input type="checkbox" checked={outputKeys.includes('instagram_story')} onChange={() => toggleOutput('instagram_story')} /> Story (9:16)</label>
        </div>

        <button className="primary heroBtn" onClick={handleGenerate} disabled={loading}>{loading ? 'Generating...' : `Generate ${selectedDealers.length * outputKeys.length || ''} Creatives`}</button>
        {message && <p className="error">{message}</p>}
      </section>
    </main>

    {result && <section className="card results glass">
      <div className="resHeader">
        <h2>Generated Output</h2>
        <a className="download" href={fullUrl(result.zip_url)}><Download size={18}/> Download ZIP Bundle</a>
      </div>
      <p>{result.count} high-quality creatives generated successfully.</p>
      <div className="previewGrid">
        {result.files.slice(0, 12).map(f => <div className="preview" key={f.url}>
          <div className="imgWrap"><img src={fullUrl(f.url)} /></div>
          <div className="prevInfo">
            <strong>{f.dealer_name}</strong>
            <span>{f.output_key.replace('_', ' ')}</span>
          </div>
          <a href={fullUrl(f.url)} className="viewBtn" target="_blank">View HD</a>
        </div>)}
      </div>
    </section>}
  </div>;
}

createRoot(document.getElementById('root')).render(<App />);
