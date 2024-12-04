import {

  IconSubtask,
  IconLogout
} from "@tabler/icons-react";

import { uniqueId } from "lodash";

const Menuitems = [
  {
    navlabel: true,
    subheader: "Home",
  },

  {
    id: uniqueId(),
    title: "Tasks",
    icon: IconSubtask,
    href: "/",
  },
  {
    navlabel: true,
    subheader: "Auth",
  },
  {
    id: uniqueId(),
    title: "Logout",
    icon: IconLogout,
    href: "/authentication/logout",
  },
];

export default Menuitems;
