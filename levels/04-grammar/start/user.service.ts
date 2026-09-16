export class UserService {
  public async fetch(userId: string) {
    const response = await this.http.get("/users/" + userId);

    if (response.status !== 200) {
      throw exception("USER_FETCH_FAILED");
    }

    return response.data;
  }
}
