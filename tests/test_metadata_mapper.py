import pytest

from avalon.metadata_mapper import MetadataMapper
import avalon.database as db
import avalon.utilities as util
from avalon.data import database as db_data
from tests.data import avalon_metadata


# Initializing an instance of the MetadataMapper class should set the
# metadata property of the instance to the metadata passed at
# initialization, set the song and disc properties to None, and set the
# album and property to either None if it has not yet been added to the
# database or its database id.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_initialize_metadata_mapper_instance(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)

        assert mapper.metadata == metadata
        assert mapper.album is None
        assert mapper.disc is None
        assert mapper.song is None


# get_song() should return None if the song metadata has not yet been
# added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_song_new_song(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata.copy())
        mapper.metadata["path"] = util.format_song_file_path(metadata)

        assert mapper.get_song() is None


# get_song() should return the database id of a song if it has already
# been added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_song_existing_song(app, database_album, database_song, metadata):
    with app.app_context():
        metadata = metadata.copy()
        metadata["path"] = util.format_song_file_path(metadata)
        song_id = database_song(metadata, database_album(metadata))
        mapper = MetadataMapper(metadata)

        assert mapper.get_song() == song_id


# get_album() should return None if the album metadata has not yet been
# added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_album_new_album(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)

        assert mapper.album is None
        assert mapper.get_album() is None


# get_album() should return the database id of an album if it has
# already been added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_album_existing_album(app, database_album, metadata):
    with app.app_context():
        album_id = database_album(metadata)
        mapper = MetadataMapper(metadata)

        assert mapper.album == album_id
        assert mapper.get_album() == album_id


# get_hub() should return None if the hub metadata has not yet been
# added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_hub_new_hub(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)

        for hub in metadata["hubs"]:
            assert mapper.get_hub(hub) is None


# get_hub() should return the database id of a hub if it has already
# been added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_hub_existing_hub(app, metadata):
    with app.app_context():
        for hub in metadata["hubs"]:
            hub_id = db.execute_write_query(
                query=db_data["hubs"]["queries"]["write"],
                data=(hub,),
            )
            mapper = MetadataMapper(metadata)

            assert mapper.get_hub(hub) == hub_id


# get_disc() should return None if the disc metadata has not yet been
# added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_disc_new_disc(app, metadata):
    if metadata["multidisc"]:
        with app.app_context():
            mapper = MetadataMapper(metadata)

            assert mapper.disc is None
            assert mapper.get_disc() is None


# get_disc() should return the database id of a disc if it has already
# been added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_disc_existing_disc(app, database_album, database_disc, metadata):
    if metadata["multidisc"]:
        with app.app_context():
            disc_id = database_disc(metadata, database_album(metadata))
            mapper = MetadataMapper(metadata)

            assert mapper.get_disc() == disc_id


# get_artist() should return None if the artist metadata has not yet
# been added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_artist_new_artist(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)

        for artist in metadata["album_artists"]:
            assert mapper.get_artist(artist) is None


# get_artist() should return the database id of an artist if it has
# already been added to the database.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_get_artist_existing_artist(app, metadata):
    with app.app_context():
        for artist in metadata["album_artists"]:
            artist_id = db.execute_write_query(
                query=db_data["artists"]["queries"]["write"],
                data=(artist,),
            )
            mapper = MetadataMapper(metadata)

            assert mapper.get_artist(artist) == artist_id


# add_album() should add album metadata and set the album property of
# the instance to its database id.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_album(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)

        mapper.add_album()

        assert mapper.album is not None
        assert mapper.album == mapper.get_album()

        album = db.execute_read_query(
            query=db_data["albums"]["queries"]["read"]["all"],
            data=(mapper.album,),
        )[0]

        assert album["name"] == metadata["album"]
        assert album["release_date"] == metadata["release_date"]
        assert album["multidisc"] == metadata["multidisc"]
        assert album["single"] == metadata["single"]


# add_disc() should add disc metadata and set the disc property of the
# instance to its database id.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_disc(app, database_album, metadata):
    if metadata["multidisc"]:
        with app.app_context():
            mapper = MetadataMapper(metadata)
            mapper.album = database_album(metadata)

            mapper.add_disc()

            assert mapper.disc is not None
            assert mapper.disc == mapper.get_disc()

            disc = db.execute_read_query(
                query=db_data["discs"]["queries"]["read"]["all"],
                data=(mapper.disc,),
            )[0]

            assert disc["album_id"] == mapper.album
            assert disc["name"] == metadata["disc_name"]
            assert disc["disc_number"] == metadata["disc_number"]


# add_artists() should add artist metadata for all artists passed and
# return their database ids.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_artists_new_artists(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)

        artist_ids = mapper.add_artists(mapper.metadata["album_artists"])

        assert len(artist_ids) == len(metadata["album_artists"])

        for index, name in enumerate(metadata["album_artists"]):
            artist = db.execute_read_query(
                query=db_data["artists"]["queries"]["read"]["all"],
                data=(artist_ids[index],),
            )[0]

            assert artist_ids[index] == index + 1
            assert artist["name"] == name


# If an artist has already been added to the database, add_artists()
# should retrieve the database id of the artist rather than try to add
# the artist again.
@pytest.mark.parametrize(
    "artists1, artists2, ids1, ids2",
    (
        (
            ["2pac", "Tha Dogg Pound", "Redman", "Method Man"],
            ["Tha Dogg Pound", "Snoop Dogg"],
            [1, 2, 3, 4],
            [2, 5],
        ),
        (
            ["DMX", "The LOX", "Jay-Z"],
            ["Jay-Z", "Ja Rule", "DMX"],
            [1, 2, 3],
            [3, 4, 1],
        ),
        (
            ["UGK", "Three 6 Mafia", "Three 6 Mafia"],
            ["UGK", "UGK", "Outkast"],
            [1, 2, 2],
            [1, 1, 3],
        ),
    ),
)
def test_add_artists_existing_artists(app, artists1, artists2, ids1, ids2):
    with app.app_context():
        mapper = MetadataMapper(avalon_metadata[0])

        assert ids1 == mapper.add_artists(artists1)
        assert ids2 == mapper.add_artists(artists2)


# add_album_artists() should add artist metadata for all artists in the
# album artists field and create the database links between the album
# and each of its album artists.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_album_artists(app, database_album, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata)
        mapper.album = database_album(metadata)

        mapper.add_album_artists()

        for index, name in enumerate(metadata["album_artists"]):
            artist = db.execute_read_query(
                query=db_data["artists"]["queries"]["read"]["all"],
                data=(index + 1,),
            )[0]

            assert (
                len(
                    db.execute_read_query(
                        query=db_data["artists_albums"]["queries"]["read"]["id"],
                        data=(index + 1, mapper.album),
                    )
                )
                == 1
            )
            assert artist["name"] == name


# add_song() should add song metadata and set the song property of the
# instance to its database id.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_song(app, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata.copy())
        mapper.metadata["path"] = util.format_song_file_path(metadata)
        mapper.add_album()

        mapper.add_song()

        assert mapper.song is not None
        assert mapper.song == mapper.get_song()

        song = db.execute_read_query(
            query=db_data["songs"]["queries"]["read"]["all"],
            data=(mapper.song,),
        )[0]

        assert song["album_id"] == mapper.album
        assert song["disc_id"] == mapper.disc
        assert song["name"] == metadata["title"]
        assert song["track_number"] == metadata["track_number"]
        assert song["length"] == metadata["length"]
        assert song["path"] == util.format_song_file_path(metadata)
        assert song["source"] == metadata["source"]


# add_song_artists() should add artist metadata for all artists in the
# song artists and group members fields and create the database links
# between the song and each of its song artists.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_song_artists(app, database_album, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata.copy())
        mapper.metadata["path"] = util.format_song_file_path(metadata)
        mapper.album = database_album(metadata)
        mapper.add_song()

        mapper.add_song_artists()

        artists = metadata["song_artists"].copy()
        if "group_members" in metadata.keys():
            artists.extend(metadata["group_members"])

        for index, name in enumerate(artists):
            artist = db.execute_read_query(
                query=db_data["artists"]["queries"]["read"]["all"],
                data=(index + 1,),
            )[0]

            link = db.execute_read_query(
                query=db_data["artists_songs"]["queries"]["read"]["all"],
                data=(index + 1,),
            )[0]

            assert artist["name"] == name

            if name in metadata["song_artists"]:
                assert link["group_member"] == 0  # False in SQLite
            else:
                assert link["group_member"] == 1  # True in SQLite


# add_producers() should add artist metadata for all producers in the
# producers, coproducers, and additional producers fields and create
# the database links between the song and each of its producers.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_producers(app, database_album, metadata):
    with app.app_context():
        mapper = MetadataMapper(metadata.copy())
        mapper.metadata["path"] = util.format_song_file_path(metadata)
        mapper.album = database_album(metadata)
        mapper.add_song()

        mapper.add_producers()

        producers = metadata["producers"].copy()
        if "coproducers" in metadata.keys():
            producers.extend(metadata["coproducers"])
        if "additional_producers" in metadata.keys():
            producers.extend(metadata["additional_producers"])

        for index, name in enumerate(producers):
            producer = db.execute_read_query(
                query=db_data["artists"]["queries"]["read"]["all"],
                data=(index + 1,),
            )[0]

            link = db.execute_read_query(
                query=db_data["producers_songs"]["queries"]["read"]["all"],
                data=(index + 1,),
            )[0]

            assert producer["name"] == name

            if name in metadata["producers"]:
                assert link["coproducer"] == 0  # False in SQLite
                assert link["additional"] == 0
            elif "coproducers" in metadata.keys() and name in metadata["coproducers"]:
                assert link["coproducer"] == 1  # True in SQLite
                assert link["additional"] == 0
            else:
                assert link["coproducer"] == 0
                assert link["additional"] == 1


# add_hubs() should add hub metadata for all hubs in the hubs field
# and create the database link between the album and each of its hubs.
@pytest.mark.parametrize("metadata", avalon_metadata)
def test_add_hubs(app, database_album, metadata):
    if "hubs" in metadata.keys():
        with app.app_context():
            mapper = MetadataMapper(metadata)
            mapper.album = database_album(metadata)

            mapper.add_hubs()

            for index, name in enumerate(metadata["hubs"]):
                hub = db.execute_read_query(
                    query=db_data["hubs"]["queries"]["read"]["all"],
                    data=(index + 1,),
                )[0]

                assert (
                    len(
                        db.execute_read_query(
                            query=db_data["hubs_albums"]["queries"]["read"]["id"],
                            data=(index + 1, mapper.album),
                        )
                    )
                    == 1
                )
                assert hub["name"] == name
