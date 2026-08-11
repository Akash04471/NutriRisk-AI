import React from 'react';

const Footer = () => {
  return (
    <footer className="mt-20 border-t border-slate-200 bg-white py-8 text-slate-500 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4 text-center sm:text-left sm:flex sm:items-center sm:justify-between">
        <div className="space-y-1">
          <div className="flex items-center justify-center sm:justify-start space-x-2">
            <span className="font-extrabold text-slate-900 font-outfit text-sm">NutriRisk AI</span>
            <span>— MCA 521-4 Machine Learning CIA-III</span>
          </div>
          <p className="text-[11px] text-slate-400">
            UCI Machine Learning Repository Dataset ID 544 | Palechor & de la Hoz Manotas (2019), <em>Data in Brief</em>.
          </p>
        </div>

        <div className="text-[11px] text-slate-400">
          <p>Full-Stack React + FastAPI Architecture</p>
          <p>© 2026 Academic Open Source Project</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
