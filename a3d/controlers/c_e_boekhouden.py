import streamlit as st
from suds.client import Client
from datetime import datetime, timedelta


class E_BoekhoudenControler:
    def __init__(self):
        self.soap_url = "https://soap.e-boekhouden.nl/soap.asmx?WSDL"
        self.username = st.secrets["USERNAME"]
        self.security_code1 = st.secrets["SECURITYCODE1"]
        self.security_code2 = st.secrets["SECURITYCODE2"]
        self.response = None  

    def reset(self):
        pass

    # MAIN
    def run(self, relatiecode):
        self.haal_facturen(relatiecode)
        return self.response

    def haal_facturen(self, relatiecode):
        try:
            # Open sessie
            client, session_id = self.open_session()

            # Bereken datums
            datum_tm = datetime.now().strftime("%Y-%m-%d")
            datum_van = (datetime.now() - timedelta(days=30 * 365)).strftime("%Y-%m-%d")

            # Vraag facturen op
            get_facturen_params = {
                "SessionID": session_id,
                "SecurityCode2": self.security_code2,
                "cFilter": {
                    "Relatiecode": relatiecode,
                    "DatumVan": datum_van,
                    "DatumTm": datum_tm,
                },
            }

            facturen_response = client.service.GetFacturen(**get_facturen_params)
            self.response = facturen_response

            # Sluit sessie
            self.close_session(client, session_id)

        except Exception as e:
            self.response = f"Er is een fout opgetreden: {str(e)}"


    # DATA
    def open_session(self):
        """
        Opent een sessie bij e-Boekhouden.nl en retourneert de SOAP-client en SessionID.
        """
        client = Client(self.soap_url)
        open_session_params = {
            "Username": self.username,
            "SecurityCode1": self.security_code1,
            "SecurityCode2": self.security_code2,
        }
        response = client.service.OpenSession(**open_session_params)
        return client, response.SessionID


    def close_session(self, client, session_id):
        """
        Sluit een actieve sessie bij e-Boekhouden.nl af.
        """
        close_session_params = {
            "SessionID": session_id,
        }
        client.service.CloseSession(**close_session_params)
      
