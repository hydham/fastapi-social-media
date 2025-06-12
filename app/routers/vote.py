from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, oauth2, database, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schemas.Vote,
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    # verify post exist
    post = db.query(models.Post).filter_by(id=vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post ID doesn't exist")

    # get post-user vote
    vote_query = db.query(models.Vote).filter_by( user_id=current_user.id, post_id=post.id)
    vote_found = vote_query.first()

    if vote.dir > 0:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post already voted")
        else:
            new_vote = models.Vote(user_id=current_user.id, post_id=post.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Voted successfully"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Vote exist for the Post")
        else:
            db.delete(vote_found)
            db.commit()
            return Response(status_code=status.HTTP_200_OK, content="Vote Removed")
