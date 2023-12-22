from cloudinary.api import resources_by_ids


def get_url_from_cloudinary_storage(public_id):
    try:
        response = resources_by_ids(public_ids=[public_id])
        resources = response.get('resources', [])
        if resources:
            return resources[0].get('url')
        else:
            return None
    except Exception as e:
        print(f"Error checking public_id existence: {e}")
        return False
