import { injectable } from 'tsyringe';

@injectable()
export class EmailService {
  public async send(args: { to: string; template: string }) {
    return this.http.post(`/send`, args);
  }
}
