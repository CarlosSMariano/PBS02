import { Api } from "./Api";

export const PBS01Service = {
    getLastTouch: () => Api.request('/lastTouch'), 
    getGol: () => Api.request('/goal')
}