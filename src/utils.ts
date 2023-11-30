import { Client } from "./components/client";

export function parseDiscoveredClients(output: any[]): Client[] {
    return output.map(client => ({ mac: client.mac, host: client.hostt}))
};