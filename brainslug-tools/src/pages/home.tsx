import { Link } from 'react-router-dom';
import './home.scss';

function Home() {

    return (
        <div className="card home">
            <p className="success">Neato Brainslug</p>
            <p>
                Neato Brainslug allows local control of your Neato robot, <strong>with</strong> or <strong>without</strong>, Home Assistant.
                To make the proccess of installing the Brainslug easier, tools on this site will help you along the way. <br /> <br />

                Use <Link to="/robot">Robot Managment</Link> to connect to your robot and view live data or find errors with your device!<br />
                Use the <Link to="/flash">Web Flasher</Link> to easily flash the Brainslug firmware to your ESP32, no matter your OS!<br /><br />

                For furthur information about the project, check out the&nbsp;<a href="https://github.com/philip2809/neato-brainslug" target="_blank" rel="noopener noreferrer">GitHub repository</a> where 
                you can find full install guides!
            </p>
        </div>
    )
}

export default Home
