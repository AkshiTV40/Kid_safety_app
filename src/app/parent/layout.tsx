import Link from 'next/link';
import PrivacyConsent from '../../components/privacy-consent';

export const metadata = { title: 'Parent Portal' };

export default function ParentLayout({ children }: { children: React.ReactNode }){
  return (
    <div className="min-h-screen bg-gray-50">
      <PrivacyConsent />
      <header className="bg-white shadow-sm">
        <div className="max-w-3xl mx-auto p-4 flex items-center justify-between">
          <h1 className="font-semibold text-lg">Parent</h1>
          <nav className="flex gap-3">
            <Link className="text-sm text-blue-600" href="/parent/contacts">Contacts</Link>
            <Link className="text-sm text-blue-600" href="/parent/location">Location</Link>
            <Link className="text-sm text-blue-600" href="/parent/help">Help</Link>
          </nav>
        </div>
      </header>
      <main className="max-w-3xl mx-auto p-4">
        {children}
      </main>
    </div>
  );
}
