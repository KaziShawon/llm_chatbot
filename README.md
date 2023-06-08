## About the Project
The target of the project is to build a customized AI assistant that will help customers plan and book tours from Booking.com through natural text conversation. The subtasks are being described here:
<ol>
  <li>Utilizing a pre-trained and lightweight LLM for chat assistant. In this case <b>blenderbot-400M-distill</b> is used <a href="https://huggingface.co/facebook/blenderbot-400M-distill">Link</a>.</li>
  <li>Utilizing up a pre-trained and lightweight NER model to detect regions in chat. In this case <b>bert-base-NER</b> is used <a href="https://huggingface.co/dslim/bert-base-NER">Link</a>.</li>
  <li>Setting Up a Frondtend with Streamlit to build interactive chatting system.</li>
  <li>Building a Backend system to interact with the chat app.</li>
  <li>Utilizing Rapid API to query hotels and booking.</li>
</ol>

<div>
  <h2>General Architecture:</h2>
  <body>
    <a href="https://ibb.co/0FNNYYr"><img src="https://i.ibb.co/ZYssccx/Custom-Model-1.png" alt="Custom-Model-1" border="0"></a>
  </body>

  <body>
    It consists of three layers:
    <ol>
      <li>Frontend</li>
      <li>Backend</li>
      <li>Deep Backend</li>
    </ol>
    The Three parts are described below
  </body>
</div>

<div>
  <h2>Building Frontend</h2>
  <p>The Frontend is built with Streamlit. The working priciples are given below</p>
  <ol>
    <li>Streamlit chat is uitilized to build a chatting UI.</li>
    <li>It displays the user conversation and LLM response.</li>
    <li>User can clear the conversation and start from beginning.</li>
    <li>User can download conversation in csv format.</li>
  </ol>
</div>

<div>
  <h2>Backend</h2>
  The backend achitecture is described here:
  <body>
    The backend architecture is divided in two parts:
    <ol>
      <li>Connect with frontend with post/chat endpoint</li>
      <li>Gather Response from LLM</li>
    </ol>
    <h4>Connect and Gather Response</h4>
    <ol>
      <li>To build backend service FastApi is used.</li>
      <li>Huggingface LLM model, both for conversatinoal and NER is used to generate response.</li>
    </ol>
  </body>
</div>

<div>
  <h2>Deep-backend</h2>
  <body>
    <h4>The deep backend architecture generates required responses. The workflow is described here:</h4>
    <ol>
      <li>Check if any region query is available, if not then perform normal conversation.</li>
      <li>If region query is available then suggest best hotel and price in USD.</li>
    </ol>
  </body>
</div>

<div>
  <body>
    <h2>Working Example</h2>
    <a href="https://ibb.co/ZdNKWC9"><img src="https://i.ibb.co/sjtQyr7/Screenshot-from-2023-06-08-17-01-03.png" alt="Screenshot-from-2023-06-08-17-01-03" border="0"></a>
  </body>
  <body>
    <h4>Instruction to run app:</h4>
    <ol>
      <li>
        <code>uvicorn backend:app --reload</code>
      </li>
      <li>
        <code>streamlit run frontend.py</code>
      </li>
      <li> A pop-up will guide towards the chatting app.</li>
    </ol>
  </body>
</div>