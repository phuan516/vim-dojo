export abstract class BaseRepository<TRecord, TEntity> {
  protected prisma: any;

  public async findOne(args: { where: object }) {
    return null;
  }

  public async update(args: { where: object; values: object }) {
    return null;
  }

  public abstract toEntity(record: TRecord): TEntity;
}
