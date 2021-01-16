# Attribute Based Acces Control (ABAC) with Attribute Based Signature (ABS)

Introduction to ABAC
=============
According to the National Institute of Standards and Technology (NIST), ABAC is an access control method where access permissions to resources are granted or denied by policies which are based on assigned attributes containing values of the subject, object, environment conditions and the names of resources. The basic idea of ABAC is simple: if the entity who wants to access a resource, possess the specific attributes related to the resource as set by the administrator, then the access is granted, otherwise it is denied.
Links to Resources:
[Wikipedia](https://www.wikiwand.com/en/Attribute-based_access_control)
[Axiomatics - ABAC](https://www.axiomatics.com/attribute-based-access-control/)

Introduction to ABS
=============
ABS is a security primitive that lets a user who possesses a set of attributes, sign a message by generating a predicate that is satisfied by his attributes. This signature shows that a single user with a set of attributes that satisfied the predicate has attested to the message. It hides the attributes and all other information that can identify the user. It is suitable to implement ABS in applications that require both data authentication and the preservation of privacy.
Links to Resources:
[Wikipedia - ABS](http://cryptowiki.net/index.php?title=Attribute-Based_Signatures)
[Research paper - ABS](https://eprint.iacr.org/2010/595.pdf)

This project
=============
Proposed Model
-------------
The model works as below:
- The Distributed PIP stores the attributes of the users of the domain.
- The model carries forward the architecture of ABAC and focuses on the development of a Decentralized Policy Information Point for ABAC. This can be used to provide fine-grained authorization to share data over the internet as it makes use of attributes.
- The concept of ABS was used as a form of cryptographic scheme to ensure both identity-anonymity and attribute-anonymity which guarantees privacy for the user.

How it works
-------------
The fundamental steps of this proposed model are listed here:
- Administrator will write policies for resources. This policy will be written in a name-value pair.
- Requester from a different domain, who wants to view the resource, will get a predicate which would contain the names of attributes needed to view the resource. This predicate is generated from the attribute names in the policy of that resource as set by the administrator.
- Requester would collect the attributes needed to satisfy the predicate from their PIP. This essentially forms the base of our Decentralized PIP model. The PIPs are used to query attributes. In a multi-domain environment, different domains reside. So for collaboration, these domains would query their PIPs for attributes. All these PIPs are not controlled by a single domain rather they are controlled by their own domain. Using the attributes that are returned from the PIP, the requester would generate their claim-predicate statement. Then sign a message with the claim-predicate statement. This signing is accomplished with the open source ABS.
- The message will be sent to the domain that contains the resource using HTTP methods.
- The domain will verify the signature and permit or deny the access to the resource. This is also accomplished with the open source ABS.

Technologies Used
-------------
* Django v3.0
* Django Rest Framework
* jQuery
* Charm Crypto
* Mongodb
* SQLite3


###End
