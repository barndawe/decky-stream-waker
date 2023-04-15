import {
  ButtonItem,
  definePlugin,
  DialogButton,
  Menu,
  MenuItem,
  PanelSection,
  PanelSectionRow,
  Router,
  ServerAPI,
  showContextMenu,
  staticClasses,
} from "decky-frontend-lib";
import { VFC } from "react";
import { FaShip } from "react-icons/fa";

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
}

const StreamWaker: VFC<{ logic: WakerLogic }> = ({logic}) => {
  return (
    <PanelSection>
      <PanelSectionRow>
        <ButtonItem bottomseparator="none" layout="below" onClick={() => {logic.wake();}}>Wake!</ButtonItem>
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
