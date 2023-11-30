import { Field } from 'decky-frontend-lib';
import { VFC } from 'react';

export interface Client {
    host: string;
    mac: string;
}

export const Client: VFC<{
    client: Client
}> = ({client}) =>{
    return (
        <Field description={client.host}><span>{client.mac}</span></Field>
    );
};