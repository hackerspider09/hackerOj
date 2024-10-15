import React, { useState } from 'react';
import { AiOutlineClose } from 'react-icons/ai';

function Popups(props) {
  const [buttonPopup, setButtonPopup] = useState(false);

  return buttonPopup ? (
    <div className='popup fixed w-[350px] h-[500px] z-[1000] bg-purple-500 flex justify-center items-center rounded-[20px]'>
      <div className="popupInner flex justify-center items-center h-[100%] w-[100%] max-w-[640px] rounded-[20px]">
        <AiOutlineClose size={30} className='close-btn text-white absolute top-[36px] right-[36px]' onClick={() => setButtonPopup(false)} />
        {props.children}
      </div>
    </div>
  ) : null;
}

export default Popups;
