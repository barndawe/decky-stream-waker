import {
  ButtonItem,
  definePlugin,
  PanelSection,
  PanelSectionRow,
  Field,
  ServerAPI,
  staticClasses,
  sleep,
} from "decky-frontend-lib";
import { useEffect, useState, useReducer, VFC } from "react";
import { FaShip } from "react-icons/fa";
import { Client } from "./components/client"
import isEqual from "lodash.isequal";
import {parseDiscoveredClients} from "./utils"
import { Spinner } from "./components/spinner"

import logo from "../assets/logo.png";

// interface AddMethodArgs {
//   left: number;
//   right: number;
// }

class WakerLogic {
  serverApi: ServerAPI;

  constructor(serverApi: ServerAPI){
    this.serverApi = serverApi;
  }

  wake = async () =>{
    await this.serverApi.callPluginMethod("wake", {});
  }

  discover = async (): Promise<Client[]> =>{
    const clientResponse = JSON.parse((await this.serverApi.callPluginMethod("get_clients", {})).result as string);
    return parseDiscoveredClients(clientResponse);
  }
}

const StreamWaker: VFC<{ logic: WakerLogic }> = ({logic}) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [clients, setClients] = useReducer((previousValue: Client[], newValue: Client[]) => {
    if (isEqual(newValue, previousValue)) {
      return previousValue;
    }
    return newValue;
  }, []);

  const refreshStatus = async(logic: WakerLogic, delay = 0) => {
    setLoading(true);
    await sleep(delay)
    setClients(await logic.discover());
    setLoading(false);
  };

  useEffect(() => {
    void refreshStatus(logic);
  }, []);

  return (
    <PanelSection>
      <PanelSectionRow>
        <ButtonItem bottomseparator="none" layout="below" onClick={() => {logic.wake();}}>Wake!</ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
      <ButtonItem bottomseparator="none" layout="below" onClick={() => {refreshStatus(logic);}}>Discover!<Spinner loading={loading}/></ButtonItem>
        <PanelSection>
          {clients.map(c => (
            <PanelSectionRow>
            <Client client={c} />
            </PanelSectionRow>
          ))}
        </PanelSection>
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin((serverApi: ServerAPI) => {
  let logic = new WakerLogic(serverApi);
  return {
    title: <div className={staticClasses.Title}>Decky Stream Waker</div>,
    content: <StreamWaker logic={logic} />,
    icon: <FaShip />,
    onDismount() {
    },
  };
});
