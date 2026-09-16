export class UserService {
  public async fetch(userId: string) {
    const result = await this.http.get("/api/v2/users/" + userId);

    if (result.status >= 400) {
      throw exception("USER_FETCH_FAILED");
    }

    return result.data;
  }
}
