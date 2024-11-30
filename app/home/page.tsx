
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faFacebook, faInstagram, faTwitter, faLinkedin } from '@fortawesome/free-brands-svg-icons';
// import { faPhone } from '@fortawesome/free-solid-svg-icons';
import Link from 'next/link';

export default function Home() {
    return (
        <div
            className="min-h-screen bg-cover bg-center flex flex-col justify-between"
            style={{
                backgroundImage: 'url("/newBg.jpg")', // Ensure background image is in the public folder
            }}
        >
            {/* Header Section */}
            <header className="w-full flex justify-end items-center mt-4 py-3 px-5">
                <nav className="flex items-center space-x-6">
                    {['Home', 'Gallery', 'About Us', 'Contact'].map((link) => (
                        <a
                            href={`#${link.toLowerCase().replace(/\s+/g, '-')}`}
                            key={link}
                            className="text-white hover:text-red-600 transition-all duration-500 transform hover:scale-110"
                        >
                            {link}
                        </a>
                    ))}
                    <Link href="/login" className=" text-black bg-gray-200 px-4 py-2 rounded-lg transition-all duration-500 transform hover:scale-110">
                        Login
                    </Link>
                    <Link href="/signup" className="text-white hover:text-gray-300 bg-red-600 px-4 py-2 rounded-lg transition-all duration-500 transform hover:scale-110">
                        Sign up
                    </Link>
                </nav>
            </header>

            {/* Main Content */}
            <main className="flex flex-col justify-center items-start px-10 ml-28 lg:px-20 py-6 text-white lg:w-1/2 space-y-6">
                <h1 className="text-7xl font-bold">Nutrition <span className='text-red-700'>AI</span></h1>
                <div className='text-center flex flex-col gap-4 pt-4'>
                    <h2 className="text-3xl font-bold">Welcome to Nutrition AI</h2>
                    <p className="text-lg leading-relaxed">
                        Are you ready to take charge of your health? At Your personalized nutrition, we believe that nutrition is the foundation of well-being. Whether you’re looking to lose weight, manage a health condition, or simply feel more energized, our personalized approach will help you achieve your goals.
                    </p>
                    <h2 className="text-2xl font-semibold">Services We Offer:</h2>
                    <ul className="pl-5 space-y-2">
                        <li>Personalized Nutrition Plans</li>
                        <li>Nutritional Counseling</li>
                        <li>Workshops and Resources</li>
                    </ul>
                </div>
            </main>

            {/* Chat Button */}
            <div className="fixed bottom-12 right-32">
                <Link href="/" className="inline-block bg-red-700 px-20 py-4 rounded-full text-white text-xl font-semibold transition-all duration-500 transform hover:bg-red-700 hover:scale-110">
                    Chat with us
                </Link>
            </div>

            {/* Footer Section */}
            {/* <footer className="bg-gray-900 bg-opacity-80 py-8 flex justify-center space-x-6 text-white mt-10">
                <a href="https://facebook.com" className="hover:text-red-600 transition-all duration-500 transform hover:scale-125">
                    <FontAwesomeIcon icon={faFacebook} size="2x" />
                </a>
                <a href="https://instagram.com" className="hover:text-red-600 transition-all duration-500 transform hover:scale-125">
                    <FontAwesomeIcon icon={faInstagram} size="2x" />
                </a>
                <a href="https://twitter.com" className="hover:text-red-600 transition-all duration-500 transform hover:scale-125">
                    <FontAwesomeIcon icon={faTwitter} size="2x" />
                </a>
                <a href="https://linkedin.com" className="hover:text-red-600 transition-all duration-500 transform hover:scale-125">
                    <FontAwesomeIcon icon={faLinkedin} size="2x" />
                </a>
                <a href="tel:+1234567890" className="hover:text-red-600 transition-all duration-500 transform hover:scale-125">
                    <FontAwesomeIcon icon={faPhone} size="2x" />
                </a>
            </footer> */}
        </div>
    );
}
