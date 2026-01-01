import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { QRCode } from 'react-qr-code';

export default function Authenticate() {
    const navigate = useNavigate();
    const [isAutherized, setIsAutherized] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [qrURI, setQrURI] = useState('');
    const [code, setCode] = useState('');
    const [now, setNow] = useState(0);

    useEffect(() => {
        fetch('/api/auth-status')
        .then(res => res.json())
        .then(data => {
            console.log('data is: ', data);
            setQrURI(data.uri);
            setNow(data.now);
        })
    }, []);

    useEffect(() => {
        if (isAutherized) {
            const timer = setTimeout(() => {
                navigate('/app');
                console.log('Navigating to dashboard');
            }, 1500);

            return () => clearTimeout(timer);
        }
    }, [isAutherized]);

    const handleVerify = async (event) => {
        event.preventDefault();
        setIsLoading(true);

        const response = await fetch('/api/verify-2fa', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code })
        });


        if (response.ok) {
            setIsAutherized(true);
        }
        else {
            alert('Invalid code');
        }
    }

    return (
        <div className='size-full flex flex-col min-h-screen items-center bg-linear-to-br from-slate-50 to-slate-100 dark:from-slate-900 via-slate-800 dark:to-slate-900 p-8'>
            <h1 className='text-center text-7xl font-extrabold antialiased tracking-wide mb-12 text-slate-800 dark:text-slate-100'>
                2 Factor Authentication
            </h1>

            <div className='
                w-full max-w-7xl min-h-4xl bg-[#010f44] bg-linear-to-br from-[#1e3a8a] via-[#010f44] to-[#010f44]
                rounded-4xl border-t-2 border-l-2 border-white/20 shadow-[0_20px_50px_rgba(0,0,0,0.5)]
            '>
                <div className='p-8'>
                    <div className='grid grid-cols-1 md:grid-cols-2 gap-8'>
                        {/* Left Section */}
                        <div className='flex flex-col gap-8'>
                            <div className='space-y-2'>
                                <h2 className='text-slate-700 text-3xl font-bold dark:text-zinc-50 dark:drop-shadow-[0_0_10px_rbga(255, 255, 255, 0.8)] dark:antialiased'>
                                    Scan QR Code To Enter Dashboard
                                </h2>
                            </div>

                            <div className='space-y-4'>
                                <div className='space-y-2'>

                                    <form onSubmit={handleVerify} className='flex flex-col gap-6'>
                                        <label
                                            htmlFor='code'
                                            className='text-slate-700 font-bold dark:text-slate-300 text-2xl'
                                        >
                                            Enter The 6-Digit Code
                                        </label>

                                        <input
                                            id="code"
                                            name='code'
                                            type='num'
                                            maxLength={6}
                                            placeholder='Enter the 6-digit code'
                                            onChange={(event) => setCode(event.target.value)}
                                            className='
                                                w-1/2 placeholder:text-center placeholder:tracking-normal placeholder:text-white/40 py-3 focus-ring-2 outline-none focus:outline-none
                                                focus:bg-blue-950 focus:shadow-[0_0_20px_rgba(59, 130, 246, 0.4)] focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-[#001b7e]
                                                transition-all duration-300 font-mono tracking-[0.5em] ring-blue-600 border-3 border-blue-800 rounded-xl text-white text-center
                                            '
                                            required
                                            value={code}
                                        />

                                        <button
                                            className='bg-blue-600 py-3.5 px-7 text-white text-center text-xl w-fit rounded-4xl shadow-xl flex flex-row justify-center items-center gap-3 disabled:cursor-not-allowed disabled:opacity-80'
                                            type='submit'
                                            disabled={isLoading}
                                        >
                                            {isLoading ? (
                                                <>
                                                    <div className='h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent' />
                                                    <span className='text-xl'>Verifying</span>
                                                </>
                                            ) : "Verify" }
                                        </button>
                                    </form>

                                </div>
                            </div>

                            <div className='pt-4 border-t border-slate-200 dark:border-slate-700'>
                                <p className='text-slate-500 dark:text-slate-400'>
                                    💡 Tip: You can scan the QR code with your phone's camera to quickly access the content.
                                </p>
                            </div>

                            <div className='pt-4 bordet-t border-slate-200 dark:border-slate-700'>
                                <p className='text-slate-500 dark:text-slate-400 opacity-25'>
                                    Can't Scan ? Manual Code: {now}
                                </p>
                            </div>
                        </div>

                        {/* right side */}
                        <div className='flex items-center justify-center p-8 bg-white dark:bg-slate-800 rounded-4xl border-2 border-slate-200 dark:border-slate-700'>
                            <div className='p-4 bg-white rounded-lg'>
                                {qrURI ? (
                                    <QRCode
                                        value={qrURI}
                                        size={200}
                                        level='H'
                                        bgColor='#FFFFFF'
                                        fgColor='#000000'
                                    />
                                ) : (
                                    <div className='w-[200px] h-[200px] flex items-center justify-center text-black font-mono text-center'>GENERATING...</div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}