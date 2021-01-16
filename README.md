# Attribute Based Acces Control (ABAC) with Attribute Based Signature (ABS)

Introduction to ABAC
=============
According to the National Institute of Standards and Technology (NIST), ABAC is an access control method where access permissions to resources are granted or denied by policies which are based on assigned attributes containing values of the subject, object, environment conditions and the names of resources. The basic idea of ABAC is simple: if the entity who wants to access a resource, possess the specific attributes related to the resource as set by the administrator, then the access is granted, otherwise it is denied.
Links to Resources: [Wikipedia](https://www.wikiwand.com/en/Attribute-based_access_control)
[Axiomatics - ABAC](https://www.axiomatics.com/attribute-based-access-control/)

Introduction to ABS
=============
ABS is a security primitive that lets a user who possesses a set of attributes, sign a message by generating a predicate that is satisfied by his attributes. This signature shows that a single user with a set of attributes that satisfied the predicate has attested to the message. It hides the attributes and all other information that can identify the user. It is suitable to implement ABS in applications that require both data authentication and the preservation of privacy.
Links to Resources: [Wikipedia - ABS](http://cryptowiki.net/index.php?title=Attribute-Based_Signatures)
[Research paper - ABS](https://eprint.iacr.org/2010/595.pdf)


###End
