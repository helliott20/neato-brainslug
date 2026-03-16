import './header.scss';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.svg';
import github from '../assets/github.svg';

function Header() {
    const navigate = useNavigate();

    return (
        <div className="header">
            <button className="nav-btn" onClick={() => navigate('/robot')}>Robot Management</button>
            <div className="logo">
                <img src={logo} alt="Brainslug Logo" height={80} />
                <div className="logo-text">
                    <span>Brainslug Tools</span>
                    <span className=''>Tools to flash and manage your brainslug</span>
                </div>
                <a href="http://github.com/philip2809/neato-brainslug" target="_blank" rel="noopener noreferrer">
                    <img src={github} alt="GitHub Logo" height={30} className="github" />
                </a>
            </div>
            <button className="nav-btn" onClick={() => navigate('/flash')}>ESP Flasher</button>
        </div>
    )
}

export default Header
